from numpy import ndarray, array

from docbr.core._unicode import un_digit_extractor, un_digit_retriever, un_formatter, un_null_validator, un_remove_separator
from docbr.core._calc import calc_repeated_check, calc_dig_validator, calc_dig_generator, calc_federal_unit_validator
from docbr.core._dict import bulk_function_applier, dict_key_selector
from docbr.core._regex import re_searcher

class Doc():
    def __init__(self, params: dict) -> None:
        self.__category   = params.get('DocCategory')
        self.__doc_len    = params.get('DocLen')
        self.__doc_attr   = params.get('DocAttributes')
        self.__dig_fu     = params.get('DigFederalState')
        self.__dig_mod    = params.get('DigModulo')
        self.__dig_oper   = params.get('DigOperation')
        self.__dig_spop   = params.get('DigSpecialOperations')
        self.__dig_seq    = params.get('DigSequence')
        self.__frmat_str  = params.get('DocFormat')
        self.__frmat_fnc  = params.get('DocFormatFunction')
        self.__doc_pttrn  = params.get('DocPattern')
        self.__doc_remspc = params.get('RemoveSpecial')
    
    def __input_handler(self, doc: ndarray, lazy: bool = False) -> None:
        self.__doc = doc
        self.__valid = array([True] * len(self.__doc))
        if self.__category == 'CheckDigit':
            if not lazy:
                self.__doc = un_digit_extractor(self.__doc, self.__doc_len)
            self.__dig = un_digit_retriever(self.__doc)

    def __output_handler(self) -> None:
        if self.__category == 'CheckDigit':
            self.__valid &= calc_repeated_check(self.__dig)
        elif self.__category == 'RegExr':
            self.__doc = array(self.__doc, dtype=object)
            self.__doc[self.__doc=='None'] = None
        
        self.__doc[~self.__valid] = None

    def __format_doc(self) -> None:
        if self.__frmat_str is not None:
            self.__doc = un_formatter(self.__doc, self.__frmat_str)
        elif self.__frmat_fnc is not None:
            self.__doc = self.__frmat_fnc(self.__doc)

    def parse(self, doc: ndarray, mask: bool) -> ndarray:
        self.__input_handler(doc)
        
        if self.__category == 'RegExr':
            self.__doc = re_searcher(self.__doc, self.__doc_pttrn, return_values=True)
            self.__valid = un_null_validator(self.__doc, na='')
            if self.__doc_remspc:
                self.__doc = un_remove_separator(self.__doc)
            self.__doc = array(self.__doc, dtype=object)
        
        if mask:
            self.__format_doc()
        self.__output_handler()
        return self.__doc

    def validate(self, doc: ndarray, lazy: bool) -> ndarray:
        self.__input_handler(doc, lazy)
        
        if self.__category == 'CheckDigit':
            self.__cv_dig = calc_dig_generator(self.__dig, self.__dig_seq, self.__dig_mod, self.__dig_oper, self.__dig_spop)
            self.__valid &= calc_dig_validator(self.__dig, self.__cv_dig)
            if self.__dig_fu is not None:
                self.__valid &= calc_federal_unit_validator(self.__dig, self.__dig_fu)
        
        elif self.__category == 'RegExr':
            self.__doc = re_searcher(self.__doc, self.__doc_pttrn, return_values=False)
            self.__valid = un_null_validator(self.__doc, na='None')

        self.__output_handler()
        return self.__valid       

    def attributes(self, doc: ndarray, attrs: list) -> ndarray:
        is_unique = len([k for k in [*dict.fromkeys(attrs)] if k in self.__doc_attr.keys()]) == 1
        self.__input_handler(doc)
        
        if self.__category == 'RegExr':
            self.__doc = re_searcher(self.__doc, self.__doc_pttrn, return_values=True)
            if self.__doc_remspc:
                self.__doc = un_remove_separator(self.__doc)
            self.__valid = un_null_validator(self.__doc, na='')

        self.__doc_attr = dict_key_selector(attrs, self.__doc_attr)
        self.__doc = bulk_function_applier(self.__doc, self.__doc_attr, is_unique)

        self.__output_handler()
        return self.__doc
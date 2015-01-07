# -*- coding: utf-8 -*-

from ..shared.model_names import(
    MODEL_NAME_FIELD, RECORD_ID_FIELD,
    PRODUCT_PRODUCT_TABLE, PRODUCT_IS_PRODUCT_VARIANT_FIELD,
    PRODUCT_ATTRIBUTE_VALUE_IDS_FIELD, AMAZON_SYNC_ACTIVE_FIELD,
    PRODUCT_DEFAULT_CODE_FIELD, PRODUCT_VARIANT_COUNT_FIELD,
    PRODUCT_NAME_FIELD,
)


class OdooProductAccess(object):
    """
    This class provides accessing services to Odoo product template
    and variant tables.
    """
    def __init__(self, env):
        self._env = env

    def is_existed(self, header):
        model_name = header[MODEL_NAME_FIELD]
        record_id = header[RECORD_ID_FIELD]
        table = self._env[model_name]
        return bool(table.browse(record_id).exists())

    def is_partial_variant(self, header):
        """
        Find if a variant is part of its template. If it is
        a variant AND doesn't have attribute value ids, it is a
        partial variant. Otherwise, return False.
        A partial variant is not an independent variant that has attributes.
        :param header: a header that has model name and record id
        :return: True if it's a partial variant, else False
        """
        result = False
        if header[MODEL_NAME_FIELD] == PRODUCT_PRODUCT_TABLE:
            record = self.browse(header)
            if not record[PRODUCT_ATTRIBUTE_VALUE_IDS_FIELD]:
                result = True
        return result

    @staticmethod
    def is_product_variant(product):
        return product[PRODUCT_IS_PRODUCT_VARIANT_FIELD]

    @staticmethod
    def has_multi_variants(product):
        result = False
        if OdooProductAccess.is_product_variant(product):
            if product[PRODUCT_VARIANT_COUNT_FIELD] > 1:
                result = True
        return result

    @staticmethod
    def generate_sku(record_id):
        # generate SKU for a product template that has multiple variants
        return 'Template_' + str(record_id)

    def browse(self, header):
        model = self._env[header[MODEL_NAME_FIELD]]
        record = model.browse(header[RECORD_ID_FIELD])
        return record

    def is_sync_active(self, header):
        record = self.browse(header)
        sync_active = record[AMAZON_SYNC_ACTIVE_FIELD]
        return sync_active

    def get_sku(self, header):
        record = self.browse(header)
        sku = record[PRODUCT_DEFAULT_CODE_FIELD]
        return sku

    def get_attributes(self, product):
        result = []
        rel_attr_table = product[PRODUCT_ATTRIBUTE_VALUE_IDS_FIELD]
        for attr_value in rel_attr_table:
            value = attr_value[PRODUCT_NAME_FIELD]
            name = attr_value['attribute_id'][PRODUCT_NAME_FIELD]
            result.append((name, value))
        return result
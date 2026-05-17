import numpy as np
import henumpy as hp


def fill_binop(left : hp.CipherArray, right : hp.CipherArray, fill_value : hp.CipherArray):
    """
    If a non-None fill_value is given, replace null entries in left and right
    with this value, but only in positions where _one_ of left/right is null,
    not both.

    Parameters
    ----------
    left : CipherArray
    right : CipherArray
    fill_value : CipherArray

    Returns
    -------
    left : CipherArray
    right : CipherArray

    """

    if fill_value is not None and fill_value.get_cipher_type() == 1:

        if left.ndim == 1: # left.shape = right.shape
            left_append = hp.append(left, fill_value)
            right_append = hp.append(right, fill_value)
            left_new = left_append[:-1].get_base_array()
            right_new = right_append[:-1].get_base_array()
            fill_value1 = left_append.get_base_array()[-1]
            fill_value2 = right_append.get_base_array()[-1]

            left_new_mask = np.isnan(left_new)
            right_new_mask = np.isnan(right_new)

            # True ^ True = False  False ^ False = False  True ^ False = True
            # Find the positions where one of the arrays is null
            mask = left_new_mask ^ right_new_mask

            if left_new_mask.any():
                left_new[left_new_mask & mask] = fill_value1

            if right_new_mask.any():
                right_new[right_new_mask & mask] = fill_value2  
            
            left = hp.CipherArray(left_new)
            right = hp.CipherArray(right_new)

        elif left.ndim == 2: # left.shape = right.shape
            fill_value_full = hp.full(left.shape[1], fill_value).cipherReshape(1, -1, output_encrypt_type=1)
            left_append = hp.append(left, fill_value_full, axis=0)
            right_append = hp.append(right, fill_value_full, axis=0)

            fill_value1 = left_append.get_base_array()[-1]
            fill_value2 = right_append.get_base_array()[-1]
            left_new = left_append[:-1].get_base_array()
            right_new = right_append[:-1].get_base_array()

            left_base_mask = np.isnan(left_new)
            right_base_mask = np.isnan(right_new)
            mask  = left_base_mask ^ right_base_mask
            for i in range(left_new.shape[1]):
                if left_base_mask[:, i].any():
                    left_newi = left_new[:, i]
                    left_newi[left_base_mask[:, i] & mask[:, i]] = fill_value1[i]
                    left_new[:, i] = left_newi
                if right_base_mask[:, i].any():
                    right_newi = right_new[:, i]
                    right_newi[right_base_mask[:, i] & mask[:, i]] = fill_value2[i]
                    right_new[:, i] = right_newi
            left = hp.CipherArray(left_new)
            right = hp.CipherArray(right_new)

    return left, right


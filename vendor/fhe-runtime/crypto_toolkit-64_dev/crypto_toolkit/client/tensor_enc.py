from ctypes import *
import numpy as np
from .base import _encrypt_tensor, _decrypt_tensor


__all__ = ['encrypt_tensor', 'decrypt_tensor', 'encrypt_image_for_plot', 'make_cipher_tensor']


def encrypt_tensor(a, method='ht', requires_grad=False):
    if method == 'ht':
        return encrypt_tensor_ht(a, requires_grad)
    elif method == 'ht2':
        return encrypt_tensor_ht2(a, requires_grad)
    else:
        raise ValueError(f"Invalid method: {method}")


def decrypt_tensor(a, method='ht', requires_grad=False):
    if method == 'ht':
        return decrypt_tensor_ht(a, requires_grad)
    elif method == 'ht2':
        return decrypt_tensor_ht2(a, requires_grad)
    else:
        raise ValueError(f"Invalid method: {method}")


def encrypt_image_for_plot(image, method='ht'):
    if method == 'ht':
        return encrypt_image_for_plot_ht(image)
    elif method == 'ht2':
        return encrypt_image_for_plot_ht2(image)
    else:
        raise ValueError(f"Invalid method: {method}")

#######################################################
################encrypt_tensor_for_ht##################
#######################################################

def is_sparse(matrix):
    if 'torch' not in dir():
        import torch

    return matrix.layout != torch.strided


# 加密tensor
def encrypt_tensor_ht(a, requires_grad=False):

    if 'hetorch' not in dir():
        import hetorch

    if 'torch' not in dir():
        import torch

    if is_sparse(a):
        a = a.coalesce()
        indices = a.indices()
        values = a.values()
        sizes = a.size()
        arr = _encrypt_tensor(values.flatten().contiguous())
        enc_values = torch.from_numpy(arr).to(torch.float64).reshape(list(values.shape) + [2])
        enc_values.requires_grad = requires_grad
        enc_ = torch.sparse_coo_tensor(indices, enc_values, list(sizes) + [2], dtype=torch.float64)
        return hetorch.CipherTensor(enc_.coalesce())
    else:
        enc_tensor = _encrypt_tensor(a.flatten().contiguous())
        res = torch.from_numpy(enc_tensor).to(torch.float64).reshape(list(a.shape) + [2])
        res.requires_grad = requires_grad
        return hetorch.CipherTensor(res)


# 解密tensor
def decrypt_tensor_ht(a, requires_grad=False):
    if 'torch' not in dir():
        import torch

    if is_sparse(a):
        a = a.coalesce()
        indices = a.indices()
        values = a.values()
        sizes = a.size()
        dec_value = None
        ori_shape = list(values.shape)
        if len(ori_shape) == 1:
            dec_value = torch.tensor(_decrypt_tensor(values.detach().numpy()), dtype=torch.float32)
        else:
            ret = _decrypt_tensor(values.flatten())
            dec_value = torch.from_numpy(ret).to(torch.float32).reshape(list(values.shape[:-1]))
            dec_value.requires_grad = requires_grad
        dec_ = torch.sparse_coo_tensor(indices, dec_value, list(sizes[:-1]), dtype=torch.float32)
        return dec_.coalesce()
    else:
        ori_shape = list(a.shape)
        if len(ori_shape) == 1:
            return torch.tensor(_decrypt_tensor(a.detach().numpy()), dtype=torch.float32)
        else:
            dec_tensor = _decrypt_tensor(a.flatten())
            res = torch.from_numpy(dec_tensor).to(torch.float32).reshape(a.shape[:-1])
            res.requires_grad = requires_grad
            return res


# 图像加密方法，不可用于模型训练，仅用于可视化，模型训练请使用encrypt_tensor方法
# 图像数据加密后是高维矩阵数据，本身是不具有打印展示意义的，这里做了简单降维处理以做到类似打印密文图像的功能
def encrypt_image_for_plot_ht(image):
    from PIL import Image
    if 'torch' not in dir():
        import torch    
    data = None
    if isinstance(image, str):
        data = Image.open(image)
        data = torch.from_numpy(np.array(data))
    elif isinstance(image, torch.Tensor):
        data = image
    elif isinstance(image, np.ndarray):
        data = torch.from_numpy(image)
    
    if data is None:
        raise ValueError("Unsupported image type. The image must be a file path, a torch.Tensor, or a numpy.ndarray.")
    
    encrypted_tensor = encrypt_tensor(data)
    norm_img = encrypted_tensor.sum(axis=-1) % 255
    norm_img = norm_img.to(torch.int64)
    
    return norm_img


def make_cipher_tensor(*shape):
    if 'hetorch' not in dir():
        import hetorch
    return hetorch.CipherTensor(hetorch.op.random(shape=tuple(list(shape))))


########################################################
################encrypt_tensor_for_ht2##################
########################################################

# 加密tensor
def encrypt_tensor_ht2(a, requires_grad=False):

    if 'hetorch2' not in dir():
        import hetorch2

    if 'torch' not in dir():
        import torch

    if is_sparse(a):
        a = a.coalesce()
        indices = a.indices()
        values = a.values()
        sizes = a.size()
        arr = _encrypt_tensor(values.flatten().contiguous())
        enc_values = torch.from_numpy(arr).to(torch.float64).reshape(list(values.shape) + [2])
        enc_values.requires_grad = requires_grad
        enc_ = torch.sparse_coo_tensor(indices, enc_values, list(sizes) + [2], dtype=torch.float64)
        return hetorch2.CipherTensor(enc_.coalesce())
    else:
        enc_tensor = _encrypt_tensor(a.flatten().contiguous())
        res = torch.from_numpy(enc_tensor).to(torch.float64).reshape(list(a.shape) + [2])
        res.requires_grad = requires_grad
        return hetorch2.CipherTensor(res)


# 解密tensor
def decrypt_tensor_ht2(a, requires_grad=False):
    if 'torch' not in dir():
        import torch

    if is_sparse(a):
        a = a.coalesce()
        indices = a.indices()
        values = a.values()
        sizes = a.size()
        dec_value = None
        ori_shape = list(values.shape)
        if len(ori_shape) == 1:
            dec_value = torch.tensor(_decrypt_tensor(values.detach().numpy()), dtype=torch.float32)
        else:
            ret = _decrypt_tensor(values.flatten())
            dec_value = torch.from_numpy(ret).to(torch.float32).reshape(list(values.shape[:-1]))
            dec_value.requires_grad = requires_grad
        dec_ = torch.sparse_coo_tensor(indices, dec_value, list(sizes[:-1]), dtype=torch.float32)
        return dec_.coalesce()
    else:
        ori_shape = list(a.shape)
        if len(ori_shape) == 1:
            return torch.tensor(_decrypt_tensor(a.detach().numpy()), dtype=torch.float32)
        else:
            dec_tensor = _decrypt_tensor(a.flatten())
            res = torch.from_numpy(dec_tensor).to(torch.float32).reshape(a.shape[:-1])
            res.requires_grad = requires_grad
            return res


# 图像加密方法，不可用于模型训练，仅用于可视化，模型训练请使用encrypt_tensor方法
# 图像数据加密后是高维矩阵数据，本身是不具有打印展示意义的，这里做了简单降维处理以做到类似打印密文图像的功能
def encrypt_image_for_plot_ht2(image):
    from PIL import Image
    if 'torch' not in dir():
        import torch    
    data = None
    if isinstance(image, str):
        data = Image.open(image)
        data = torch.from_numpy(np.array(data))
    elif isinstance(image, torch.Tensor):
        data = image
    elif isinstance(image, np.ndarray):
        data = torch.from_numpy(image)
    
    if data is None:
        raise ValueError("Unsupported image type. The image must be a file path, a torch.Tensor, or a numpy.ndarray.")
    
    encrypted_tensor = encrypt_tensor2(data)
    norm_img = encrypted_tensor.sum(axis=-1) % 255
    norm_img = norm_img.to(torch.int64)
    
    return norm_img




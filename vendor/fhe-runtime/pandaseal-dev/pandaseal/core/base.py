import numpy as np

FLOAT_EQUAL_RTOL = 1e-12


def _group_and_replace(arr):
    """
    For 1D or 2D ndarray data, group and normalize elements.
    For 1D data, maintain the original order.
    For 2D data, operate column by column, treating each column independently.
    """
    def process_column(column):
        is_nan = np.isnan(column)
        # Sort the array and get the sorted indices
        sorted_indices = np.argsort(column)
        sorted_col = column[sorted_indices]
        
        # Initialize the result array
        grouped_col = np.copy(sorted_col)
        
        # Traverse and group the data
        group_start = 0
        for i in range(1, len(sorted_col)):
            current = sorted_col[i]
            group_start_value = sorted_col[group_start]
            
            # Iteratively divide by 1024 until both values are less than 1000
            while abs(current) > 1000. or abs(group_start_value) > 1000.:
                current /= 1024.0
                group_start_value /= 1024.0
            
            # Compute the difference between the current value and the group start value
            diff = abs(current - group_start_value)
            
            # Check if the difference is within the tolerance
            if diff > FLOAT_EQUAL_RTOL:
                group_start = i  # Update the group start index
            
            # Replace the current value with the group start value
            grouped_col[i] = grouped_col[group_start]
        
        # Restore the original order
        result = np.zeros_like(column)
        result[sorted_indices] = grouped_col
        result[is_nan] = np.nan
        return result

    # Check the dimensionality of the input array
    if arr.ndim == 1:
        # Process directly for 1D input
        return process_column(arr)
    elif arr.ndim == 2:
        # For 2D input, process each column independently
        result = np.zeros_like(arr)
        for col_idx in range(arr.shape[1]):
            result[:, col_idx] = process_column(arr[:, col_idx])
        return result
    else:
        raise ValueError("Input array must be 1D or 2D.")
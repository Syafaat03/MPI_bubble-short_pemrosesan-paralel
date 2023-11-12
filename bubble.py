from mpi4py import MPI

def parallel_bubble_sort(arr):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_arr = arr[rank::size]

    for i in range(len(local_arr)):
        for j in range(0, len(local_arr) - i - 1):
            if local_arr[j] > local_arr[j + 1]:
                local_arr[j], local_arr[j + 1] = local_arr[j + 1], local_arr[j]

    sorted_arr = comm.gather(local_arr, root=0)

    if rank == 0:
        combined_arr = [item for sublist in sorted_arr for item in sublist]
        combined_arr.sort()
        for i in range(len(arr)):
            arr[i] = combined_arr[i]

if _name_ == '_main_':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        arr = [5, 3, 4, 1, 2]
    else:
        arr = None

    arr = comm.bcast(arr, root=0)  # Broadcast the arr from rank 0 to all nodes

    comm.barrier()

    parallel_bubble_sort(arr)

    if rank == 0:
        print(f"List sorted with bubble sort in ascending order: {arr}")

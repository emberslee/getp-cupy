import numpy as np
import mrcfile

def read_mrc(filename, ignorestart=False):
    return read_map(filename, ignorestart)

def read_map(filename, ignorestart=False):
    mrc = mrcfile.open(filename, mode='r')
    data = np.asarray(mrc.data.copy(), dtype=np.float32)
    voxel_size = np.asarray([mrc.voxel_size.x, mrc.voxel_size.y, mrc.voxel_size.z], dtype=np.float32)
    ncrsstart = np.asarray([mrc.header.nxstart, mrc.header.nystart, mrc.header.nzstart], dtype=np.float32)
    origin = np.asarray([mrc.header.origin.x, mrc.header.origin.y, mrc.header.origin.z], dtype=np.float32)
    ncrs = (mrc.header.nx, mrc.header.ny, mrc.header.nz)
    angle = np.asarray([mrc.header.cellb.alpha, mrc.header.cellb.beta, mrc.header.cellb.gamma], dtype=np.float32)
    mapcrs = np.asarray([mrc.header.mapc, mrc.header.mapr, mrc.header.maps], dtype=np.int32)
    mrc.close()

    assert(np.all(angle == 90.0))

    ''' reorder axes

        mapcrs-1    sort        transpose
        0, 1, 2 --> 0, 1, 2 --> 0, 1, 2
        0, 2, 1 --> 0, 2, 1 --> 1, 0, 2
        1, 0, 2 --> 1, 0, 2 --> 0, 2, 1
        1, 2, 0 --> 2, 0, 1 --> 1, 2, 0
        2, 0, 1 --> 1, 2, 0 --> 2, 0, 1
        2, 1, 0 --> 2, 1, 0 --> 2, 1, 0

    '''
    sort = np.asarray([0, 1, 2], dtype=np.int32)
    for i in range(3):
        sort[mapcrs[i] - 1] = i
    nxyzstart = np.asarray([ncrsstart[i] for i in sort], dtype=np.int32)
    nxyz = np.asarray([ncrs[i] for i in sort], dtype=np.int32)
    data = np.transpose(data, axes=2-sort[::-1])

    ''' shift map origins '''
    if not ignorestart:
        origin += np.multiply(nxyzstart, voxel_size)

    return data, origin, voxel_size


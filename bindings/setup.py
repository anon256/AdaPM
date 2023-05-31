from setuptools import setup, Extension
from torch.utils import cpp_extension
import os

##############################################
#
#   PyTorch bindings to AdaPM
#
##############################################

# helpful info on this: https://docs.python.org/3/distutils/setupscript.html

pm_dir = '../'
# we need absolute paths at least for the so-links to protobuf-lite and zmq
pm_dir = os.path.abspath(pm_dir)+'/'
deps_dir = pm_dir + 'deps_bindings/'

# include_dirs = cpp_extension.include_paths() # get default include dirs
pm_include_dirs = [pm_dir,
                      pm_dir + 'src',
                      pm_dir + 'include',
                      deps_dir + 'include']

setup(name='pm',
      version='0.1',
      description='PyTorch bindings to the AdaPM parameter server',
      ext_modules=[cpp_extension.CppExtension(
          name='adapm',
          include_dirs = pm_include_dirs,
          extra_objects = [pm_dir + 'build/libps.a'],
          depends       = [pm_dir + 'build/libps.a',
                           pm_dir + 'include/ps/addressbook.h',
                           pm_dir + 'include/ps/base.h',
                           pm_dir + 'include/ps/coloc_kv_server.h',
                           pm_dir + 'include/ps/coloc_kv_server_handle.h',
                           pm_dir + 'include/ps/coloc_kv_worker.h',
                           pm_dir + 'include/ps/kv_app.h',
                           pm_dir + 'include/ps/ps.h',
                           pm_dir + 'include/ps/sync_manager.h',
                           pm_dir + 'include/ps/sampling.h',
                          ],
          # The linking we do below in `extra_link_args` would probably be cleaner with
          # `runtime_library_dirs` and `libraries`, but I did not get that to work.
          extra_link_args = ['-Wl,-rpath,'+deps_dir+'lib',
                             '-L'+deps_dir+'lib',
                             '-lprotobuf-lite',
                             '-lzmq'],
          sources=['bindings.cc'],
          extra_compile_args=['-DKEY_TYPE=int64_t'],
          # define_macros=[('NDEBUG', '1')],
      )],
      cmdclass={'build_ext': cpp_extension.BuildExtension})


import config
from install_package import InstallPackage
import os
import shutil
import utils

BASENAME = "vtkdevide"
SVN_REPO = "https://stockholm.twi.tudelft.nl/svn/devide/trunk/" + BASENAME

class VTKDEVIDE(InstallPackage):
    
    def __init__(self):
        self.source_dir = os.path.join(config.build_dir, BASENAME)
        self.build_dir = os.path.join(config.build_dir, '%s-build' %
                                      (BASENAME,))
        self.inst_dir = os.path.join(config.inst_dir, BASENAME)

    def get(self):
        if os.path.exists(self.source_dir):
            utils.output("vtkdevide already checked out, skipping step.")

        else:
            os.chdir(config.build_dir)
            ret = os.system("%s co %s" % (config.SVN, SVN_REPO))
            if ret != 0:
                utils.error("Could not SVN checkout.  Fix and try again.")

    def unpack(self):
        # no unpack step
        pass

    def configure(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'CMakeFiles/cmake.check_cache')):
            utils.output("vtkdevide build already configured.")
            return
        
        if not os.path.exists(self.build_dir):
            os.mkdir(self.build_dir)

        os.chdir(self.build_dir)
        cmake_params = "-DBUILD_SHARED_LIBS=ON " \
                       "-DBUILD_TESTING=OFF " \
                       "-DCMAKE_BUILD_TYPE=RelWithDebInfo " \
                       "-DCMAKE_INSTALL_PREFIX=%s " \
                       "-DVTK_DIR=%s " \
                       "-DDCMTK_INCLUDE_PATH=%s " \
                       "-DDCMTK_LIB_PATH=%s" % \
                       (self.inst_dir, config.VTK_DIR,
                        config.DCMTK_INCLUDE, config.DCMTK_LIB)

        ret = os.system("%s %s %s" %
                        (config.CMAKE, cmake_params, self.source_dir))

        if ret != 0:
            utils.error("Could not configure vtkdevide.  Fix and try again.")
        

    def build(self):
        if os.path.exists(
            os.path.join(self.build_dir, 'bin/libvtkdevideExternalPython.so')):

            utils.output("vtkdevide already built.  Skipping build step.")

        else:
            os.chdir(self.build_dir)
            ret = os.system("%s" % (config.MAKE,))
            if ret != 0:
                utils.error("Could not build vtkdevide.  Fix and try again.")
        

    def install(self):
        config.VTKDEVIDE_LIB = os.path.join(self.build_dir, 'bin')
        config.VTKDEVIDE_PYTHON = os.path.join(
            self.source_dir, 'Wrapping/Python')

    def clean_build(self):
        # nuke the build dir, the source dir is pristine and there is
        # no installation
        shutil.rmtree(self.build_dir)
        
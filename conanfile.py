from conans import CMake, ConanFile, AutoToolsBuildEnvironment, tools
import os
import shutil

class OggConan(ConanFile):
    name = "ogg"
    version = "1.3.2"
    ZIP_FOLDER_NAME = "lib" + name + "-" + version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["CMakeLists.txt", "FindOgg.cmake"]
    url="http://github.com/GatorQue/conan-ogg"
    license="MIT License"
    description="OGG is an open source audio codec."

    def source(self):
        zip_name = "lib%s-%s.tar.gz" % (self.name, self.version)
        tools.download("http://downloads.xiph.org/releases/ogg/%s" % zip_name, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os == "Windows":
            shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.ZIP_FOLDER_NAME)

    def build(self):
        if self.settings.os == "Windows":
            cmake = CMake(self.settings)

            cmake_options = []
            cmake_options.append("-DCMAKE_INSTALL_PREFIX:PATH=../install")
            if self.options.shared == True:
                cmake_options.append("-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=ON")
                cmake_options.append("-DBUILD_SHARED_LIBS=ON")

            self.run("IF not exist build mkdir build")
            cd_build = "cd build"
            self.output.warn('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.run('%s && cmake ../%s %s %s' % (cd_build, self.ZIP_FOLDER_NAME, cmake.command_line, " ".join(cmake_options)))
            self.output.warn('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
            self.run('%s && cmake --build . --target install %s' % (cd_build, cmake.build_config))
        else:
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = self.options.shared

            if self.settings.os == "Macos":
                old_str = '-install_name \$rpath/\$soname'
                new_str = '-install_name \$soname'
                tools.replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)

            conf_options = []
            conf_options.append("--prefix=/")
            if self.options.shared == True:
                conf_options.append("--enable-shared")
                conf_options.append("--disable-static")
            else:
                conf_options.append("--disable-shared")
                conf_options.append("--enable-static")

            with tools.environment_append(env_build.vars):
                self.run("./configure %s" % " ".join(conf_options), cwd=self.ZIP_FOLDER_NAME)
                self.run("make", cwd=self.ZIP_FOLDER_NAME)
                self.run("make install DESTDIR=%s/install" % self.conanfile_directory, cwd=self.ZIP_FOLDER_NAME)

    def package(self):
        self.copy("FindOgg.cmake", dst=".", src=".")
        self.copy("*", dst="include", src="install/include")
        self.copy("*", dst="lib", src="install/lib", links=True)
        self.copy("*", dst="bin", src="install/bin")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["ogg"]


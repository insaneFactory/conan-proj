from conans import ConanFile, CMake, tools
import os


class Proj4Conan(ConanFile):
	name = "proj"
	version = "6.2.1"
	_datumgrid_version = "world-1.0"
	license = "MIT license"
	url = "https://github.com/insaneFactory/conan-proj"
	description = "Cartographic Projections Library"
	settings = "os", "compiler", "build_type", "arch"
	options = {
		"shared": [True, False],
		"fPIC": [True, False]
	}
	default_options = {
		"shared": False,
		"fPIC": True
	}
	build_requires = "sqlite3_installer/3.29.0@insanefactory/stable"
	requires = "sqlite3/3.29.0"
	generators = "cmake"
	_source_subfolder = "source_subfolder"
	
	def configure(self):
		if self.settings.compiler == "Visual Studio":
			del self.options.fPIC

	def source(self):
		archive = "proj-%s" % self.version
		tools.get("https://download.osgeo.org/proj/%s.tar.gz" % archive, md5="9f874e227d221daf95f7858dc55dfa3e")
		os.rename(archive, self._source_subfolder)
		
		tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "set(PROJECT_INTERN_NAME PROJ)",
						  '''set(PROJECT_INTERN_NAME PROJ)
		include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
		conan_basic_setup()''')

		with tools.chdir(os.path.join(self._source_subfolder, "data")):
			tools.get("https://download.osgeo.org/proj/proj-datumgrid-%s.zip" % self._datumgrid_version)

	def build(self):
		cmake = CMake(self)
		cmake.configure(source_folder=self._source_subfolder, defs={
			"PROJ_TESTS": False,
			"BUILD_LIBPROJ_SHARED": self.options.shared
		})
		cmake.build()
		cmake.install()

	def package(self):
		self.copy("*.pdb", dst="bin", src="bin")
		self.copy("*.pdb", dst="lib", src="lib")

	def package_info(self):
		libname = "proj"
		if self.settings.os == "Windows":
			libname += "_6_2"
			if self.settings.build_type == "Debug":
				libname += "_d"
		self.cpp_info.libs = [libname]


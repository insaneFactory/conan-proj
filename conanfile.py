from conans import ConanFile, CMake, tools


class Proj4Conan(ConanFile):
	name = "proj4"
	version = "5.2.0"
	license = "MIT license"
	url = "https://github.com/insaneFactory/conan-proj4"
	description = "Cartographic Projections Library"
	settings = "os", "compiler", "build_type", "arch"
	source_subfolder = "src"
	options = {
		"shared": [True, False],
		"fPIC": [True, False]
	}
	default_options = {
		"shared": False,
		"fPIC": True
	}
	generators = "cmake"
	
	def configure(self):
		if self.settings.compiler == "Visual Studio":
			del self.options.fPIC

	def source(self):
		self.run("git clone https://github.com/OSGeo/proj.4.git %s" % self.source_subfolder)
		self.run("cd %s && git checkout %s" % (self.source_subfolder, self.version))
		
		tools.replace_in_file("src/CMakeLists.txt", "set(PROJECT_INTERN_NAME PROJ)",
						  '''set(PROJECT_INTERN_NAME PROJ)
		include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
		conan_basic_setup()''')

	def build(self):
		cmake = CMake(self)
		cmake.configure(source_folder=self.source_subfolder, defs={
			"PROJ_TESTS": False,
			"BUILD_LIBPROJ_SHARED": self.options.shared
		})
		cmake.build()

	def package(self):
		self.copy("*.h", dst="include", src="%s/src" % self.source_subfolder)
		self.copy("*", dst="lib", src="lib")
		self.copy("*", dst="bin", src="bin")

	def package_info(self):
		libname = "proj"
		if self.settings.os == "Windows":
			libname += "_5_2"
			if self.settings.build_type == "Debug":
				libname += "_d"
		self.cpp_info.libs = [libname]


module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    release: {
      options: {
        commitMessage: 'Release <%= version %> [no ci]' //default: 'release <%= version %>
      }
    }
  });

  grunt.loadNpmTasks('grunt-release');
  grunt.registerTask('default', []);
};

var gulp = require('gulp'),
  concat = require('gulp-concat'),
  uglify = require('gulp-uglify'),
  rename = require('gulp-rename'),
  sass = require('gulp-sass')(require('sass')),
  autoprefixer = require('gulp-autoprefixer'),
  browserSync = require('browser-sync').create();

var DEST = 'build/';

gulp.task('scripts', function() {
  return gulp
    .src(['src/js/helpers/*.js', 'src/js/*.js'])
    .pipe(concat('custom.js'))
    .pipe(gulp.dest(DEST + '/js'))
    .pipe(rename({ suffix: '.min' }))
    .pipe(uglify())
    .pipe(gulp.dest(DEST + '/js'))
    .pipe(browserSync.stream());
});

var compileSASS = function(filename, options) {
  return gulp.src('src/scss/*.scss')
    .pipe(sass(options).on('error', sass.logError))
    .pipe(autoprefixer({ cascade: false }))
    .pipe(concat(filename))
    .pipe(gulp.dest(DEST + '/css'))
    .pipe(browserSync.stream());
};

gulp.task('sass', function() {
  return compileSASS('custom.css', {});
});

gulp.task('sass-minify', function() {
  return compileSASS('custom.min.css', { outputStyle: 'compressed' });
});

gulp.task('browser-sync', function(done) {
  browserSync.init({
    server: {
      baseDir: './',
      serveStaticOptions: {
        extensions: ['html']
      }
    },
    port: 80,
    notify: false,
    startPath: './bank/dashboard'
  });
  done();
});

gulp.task('watch', function() {
  gulp.watch('production/*.html', browserSync.reload);
  gulp.watch('src/js/*.js', gulp.series('scripts'));
  gulp.watch('src/scss/*.scss', gulp.series('sass', 'sass-minify'));
});

gulp.task('default', gulp.series('browser-sync', 'watch'));

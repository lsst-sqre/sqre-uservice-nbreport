import autoprefixer from 'autoprefixer';
import cleanCSS from 'gulp-clean-css';
import gulp from 'gulp';
import GulpRunner from 'gulp-run';
import minimist from 'minimist';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';
import postcss from 'gulp-postcss';

// parse command line options
// [--env dev (default) | prod]
const options = minimist(process.argv);
const env = options.env || 'dev';

// Environment-based configurations for CleanCss
// https://github.com/jakubpawlowicz/clean-css
const cleanCssConfig = {
  dev: {
    compatibility: '*',
    level: 2,
    format: 'beautify'
  },

  prod: {
    compatibility: '*',
    level: 2
  }
};

/*
 * gulp environment
 * Prints the environment setting.
 */
export const environment = () => console.log(`${env}`);

/*
 * gulp pretty
 * Run Prettier to autoformat code.
 */
export const pretty = () => {
  return GulpRunner('npm run pretty').exec();
};

/*
 * gulp sass
 * Compile the sass
 */
const sassTask = () => {
  let stream = gulp
    .src('scss/app.scss')
    // Initialize sourcemaps
    .pipe(sourcemaps.init())
    // Compile sass synchronously
    .pipe(sass.sync().on('error', sass.logError))
    // Autoprefix with default configs
    .pipe(postcss([autoprefixer()]))
    // Clean CSS
    .pipe(cleanCSS(cleanCssConfig[env]));

  if (env === 'dev') {
    // Write out sourcemaps
    stream.pipe(sourcemaps.write());
  }

  stream.pipe(gulp.dest('uservice_nbreport/publish/templates/report-html'));
  return stream;
};
gulp.task('sass', sassTask);

/*
 * gulp watch
 * Watch for source changes and rebuild any assets
 */
const watchTask = () => {
  gulp.watch('styles.scss', ['sass']);
};
gulp.task('watch', watchTask);

/*
 * gulp
 * Default task that compiles assets and watches for additional changes.
 */
gulp.task('default', ['sass', 'watch']);

import gulp from 'gulp';
import minimist from 'minimist';

// parse command line options
// [--env dev (default) | prod]
const options = minimist(process.argv);
const env = options.env || 'dev';

/*
 * gulp environment
 * Prints the environment setting.
 */
export const environment = () => console.log(`${env}`);

/*
 * gulp
 * Default task.
 */
export default environment;

import logging
#logging.disable(logging.CRITICAL) #Uncomment to disable all message output
logging.basicConfig(filename='monkey.log',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s - %(funcName)s - %(lineno)d - %(module)s')

## EXAMPLES
### use instead of print(x) for lowest level troubleshooting
#logging.debug('x is ' + str(i))

### use to record general events or confirm successful operation')
#logging.info('Currently running IMU getxyz')

### use to indicate an error that isn't the end of the world')
#logging.warning('not running as root, try again with sudo')

### use to record regular errors
#logging.error('failed to import libraries')

### highest level. something fatal has occured.
#logging.critical('halted the execution due to big dumb. pls fix')





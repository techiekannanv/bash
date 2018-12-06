from __future__ import print_function
import os.path
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

#Store the user, resource and soft/hard values
resource_limits = [
    #samle data
    #'user_name name_of_resource soft_limit [hard_limit]'
    'kannan nproc 16684',
    'poda nproc 4096',
    'vada nproc 2048 4096 1234',
    'dummy nproc 1024'
]

#Config file location
#config_dir = '/etc/security/limits.d'
config_dir = os.path.expanduser('~')
config_files = {
    'nproc':'20-nproc.conf'
}
TMP = '/tmp/kv930b/'
logging.debug('Is temp directory exists? {}'.format(os.path.exists(TMP)))


if not os.path.exists(TMP):
    logging.debug('Creating temp directory {}'.format(TMP))
    os.mkdir(TMP)
#To store the file content in the dictionary with reference of resource name
limits_file_data = {}

resources = {}
#Process the input resource_limits and format them in the form of 'user resource soft hard'
for entry in resource_limits:
    data = entry.split()


    #Skip if the input is having less than 3 fields
    if len(data) < 3:
        logging.error('Require atleast 3 fields but received {} skipping this'.format(data))
        continue


    #if the input is having only 3 fields then use soft limit as hard limit
    if len(data) == 3:
        data.append(data[-1])
    #if the input is more than 4 fields then only get 4 fields and trim rest of the fields
    elif len(data) > 4:
        logging.warning('Received more than 4 fields {} trimming it to 4'.format(data))
        data = data[:4]


    #Split the list to individual items to update
    user, resource, soft, hard = data
    if resource not in resources:
        resources[resource] = {user:(soft, hard)}
    resources[resource].update({user: (soft, hard)})


for resource in resources.keys():


    #Check if the resource data is already available in the dictionary limits_file_data
    if resource not in limits_file_data:
        #If the resource data is not available then proceed to read the data
        # Get the configuration file for resource which processing now
        file = os.path.join(config_dir, config_files[resource])
        logging.debug('Processing "{}"'.format(' '.join(data) + " " + file))
        limits_file_data[resource] = []


        with open(file) as limits_entry:
            for line in limits_entry:
                limits_file_data[resource].append(line.rstrip('\n'))
        output_file = TMP + resource
        logging.debug('Output file name is {}'.format(output_file))
        users = resources[resource].keys()


        with open(output_file, 'w') as output:
            for items in limits_file_data[resource]:
                splitted = items.split()


                if len(splitted) > 0 and splitted[0] in users:
                    user = splitted[0]
                    if splitted[1] == 'soft':
                        splitted[3] = resources[resource][user][0]
                    if splitted[1] == 'hard':
                        splitted[3] = resources[resource][user][1]
                    final = ' \t'.join(splitted)
                    logging.info('Old entry "{}"'.format(items))
                    logging.info('New entry "{}"'.format(final))
                else:
                    logging.debug('commented item {}'.format(items))
                    final = items
                output.write(final+'\n')


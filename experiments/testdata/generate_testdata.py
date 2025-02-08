# 
# Generate test point_data for the experiments

import datetime
import os
import uuid
import numpy as np
import argparse
import jinja2
import requests

# jinja2 template for the test point_data
test_template = '''\
some point point_data for the experiments with the following properties:  
- number of point_data points: {{ n }}
- point_data points are generated randomly from the uniform distribution on [0, 1]
- point_data points are stored in a text file with the following format: 
    - each row corresponds to a point_data point  
    - each column corresponds to a dimension of the point_data point
    - point_data points 
    {% for point in point_data %}
    {{ point[0]|int}}, {{ point[1]|int }}
    {% endfor %}
- the point_data file is named {{ output }}
    
'''

# Note that we do not use pyDataverse, simple post requests is all we need

def create_dataset(api_token, server_url, parent, dataset_json):
    response = requests.post(server_url + '/api/dataverses/' + parent + '/datasets', 
                  headers={'X-Dataverse-key': api_token, 'Content-type': 'application/json'}, 
                  data=dataset_json)

    response.raise_for_status()
    return response.json()


def publish_dataset(api_token, server_url, pid):
    response = requests.post(server_url + '/api/datasets/:persistentId/actions/:publish', 
                            headers={'X-Dataverse-key': api_token},
                            params={'persistentId': pid, 'type': 'major'})

    response.raise_for_status()
    return response.json()


# Generate test point_data; for the Archaeology Datastation in RD Coordinates
def generate_point_data(n):
    # generate point_data, random uniform distribution on [0, 1]
    d = 2 # fixed to 2D points
    point_data = np.random.rand(n, d)
    # scale and shift point_data to match (almost) valid RD coordinates
    # https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten
    # " de x-coördinaat tussen 0 en 280 km ligt en de y-coördinaat tussen 300 en 625 km."
    # X
    point_data[:, 0] *= 280000
    # Y
    point_data[:, 1] *= 325000
    point_data[:, 1] += 300000
    # floor to integer (meters in RD coordinates)
    point_data = np.floor(point_data)
    return point_data


# main program
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate test datasets for the experiments')
    parser.add_argument('-n', type=int, default=1, help='Number of datasets')
    parser.add_argument('-a', type=str, help='API token', required=True)
    # output is not used now
    parser.add_argument('--output', type=str, default='testdata_pids.txt', help='Output file')
    args = parser.parse_args()

    # TODO: parse from command line
    parent = 'root'
    server_url = 'https://dev.archaeology.datastations.nl'
    api_token = args.a 
    n = args.n
    output = args.output

    point_data = generate_point_data(n)


    id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")   
    

    # determine location of this python file
    path = os.path.dirname(os.path.realpath(__file__))

    # Using a template engine to generate json was simpler that using the json module and traversing the hierarchy
    with open(path + '/dataset_json.j2', 'r') as f:
         template = jinja2.Template(f.read())

    for i in range(n):
        title = 'Test dataset ' + str(i) + ' ' + id
        keyword = 'maptest ' + timestamp
        content = template.render(title=title, keyword=keyword, point=point_data[i])
        #with open('experiments/testdata/'+ 'dataset_json_'+str(i)+'.json', 'w') as f:
        #    f.write(content)
        result = create_dataset(api_token, server_url, parent, content)
        #print(result)
        print("Id: {} PID: {}".format(result['data']['id'], result['data']['persistentId']))
        # publish
        pid = result['data']['persistentId']
        result = publish_dataset(api_token, server_url, pid)
        print(result)

# TODO: save the dataset id and pid to a file for later use; like destroy
# Example bash script to destroy datasets, 24 to 33
# for id in {24..33}; 
#   do echo $i; 
#   curl -H "X-Dataverse-key: $API_TOKEN" -X DELETE "$SERVER_URL/api/datasets/$id/destroy";
# done

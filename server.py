import socket
import datetime
import time
from influxdb import InfluxDBClient



def main():
    host = '127.0.0.1'        # Symbolic name meaning all available interfaces
    port = 8080     # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    
    print host , port
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        
        try:
            data = conn.recv(1024)
            
            if not data: break
            if data!='\n':
                print "Client Says: "+data
                Parse(data)
            conn.sendall("Server Says:hi")
                
        except socket.error:
            print "Error Occured."
            break

            conn.close()


def Parse(line):
    test=line.split('\n\n')
    #print test
    for values in test:
        if values!='\n':
            #print timestamp
            #print day
            #print line
            #print timestamp_hour
            values=line.split(',')
            #print values
            
            if len(values)>1:
                timestamp=values[0].split()
                #print timestamp
                
                x=values[1]
                y=values[3]
                z=values[5]
                
                z=z.replace('\n','')
                print '-----------------------------------------'
                
                if len(timestamp)<=3:           
                    day = timestamp[0]    
                    timestamp_hour = timestamp[1][0:8]
                    #print(timestamp_hour)
                elif len(timestamp)==5:
                    day = timestamp[0]    
                    timestamp_hour = timestamp[3][0:8]
                else:
                    day = timestamp[0]    
                    timestamp_hour = timestamp[2][0:8]
                newline=str(day) + " " + str(timestamp_hour) + " " + str(x) + " " + str(y) + " " + str(z)
                    #print newline
                    
                formated_timestamp =str(day) + " "
                formated_timestamp=formated_timestamp + str(timestamp_hour)
                formated_timestamp=formated_timestamp[:6] + '20' + formated_timestamp[6:]
                #print formated_timestamp
                dt = datetime.datetime.strptime(formated_timestamp, '%d.%m.%Y %H:%M:%S')
                
                ut =time.mktime(dt.timetuple())
                
                #print ut
                Store_in_DB(x,y,z,ut)
                   
                
def Store_in_DB(x,y,z,ut,host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'root'
    password = 'root'
    dbname = 'IGUP'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select * from seismograph;'
    json_body = [
        {
            "measurement": "Magnetometer",
            "tags": {
                "Instrument": "Simple Aurora Monitor SAM",
                "units": "Tesla"
            },
            "time":int(ut),
            "fields": {
                "X": x,
                "Y": y,
                "Z": z,
                
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)


    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    #print(client)

    #print("Querying data: " + query)
    #result = client.query(query)

    #print("Result: {0}".format(result))
    
    #print json_body


if __name__ == '__main__':
    main()

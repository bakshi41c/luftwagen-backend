import traffic
import weather
#from ML.NN import setup
#get_pm5_prediction = setup()


def get_pollution_value(lat, lon, hour_offset):
    traffic_flow = traffic.get_traffic_data(lat, lon)
    print "traffic: " + str(traffic_flow)
    o3, pm25 = predict_pollution(*weather.get_weather(lat, lon, hour_offset))
    print "o3=" + str(o3) + ", pm25=" + str(pm25)

    aggregate_value = (o3 + pm25)

    return aggregate_value + ((traffic_flow / 10.0) * aggregate_value)


def get_pollution_rating(lat, lon):
    pass


def predict_pollution(precipitation_prob, relative_humidity, temp, wind_direction, wind_speed):
    o3preictedval = 5.03704930e+01 + (precipitation_prob * 9.66895471e-02) + (relative_humidity * -2.99780572e-03) + \
                    (temp * -2.26017118e-01) + (wind_direction * -8.96663780e-03) + (wind_speed * 9.98339351e+00)

    pm25predictedval = 1.36006991e+01 + (temp * -9.32461073e-02) + (wind_direction * -3.35510810e-04) + (
        wind_speed * -7.50369156e-01)

    nn_prediction = pm25predictedval  # get_pm5_prediction(TMP=temp, WDIR=wind_direction, WSPD=wind_speed)

    # 3.6 is average
    if abs(nn_prediction - pm25predictedval) > 7.2:
        if abs(nn_prediction - 3.6) > abs(pm25predictedval - 3.6):
            return o3preictedval, pm25predictedval
        else:
            return o3preictedval, nn_prediction

    return o3preictedval, (nn_prediction + pm25predictedval) / 2

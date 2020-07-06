from firebase import firebase


firebase = firebase.FirebaseApplication('https://iotfirebase-d312f.firebaseio.com/', None)
data1 =  { 'RestaurantName': 'restaurant1',
          'AvailableSeats': '4',
          'SafenessLevel': 'HighRisk'
          }
data2 =  { 'RestaurantName': 'restaurant2',
          'AvailableSeats': '3',
          'SafenessLevel': 'HighRisk'
          }
data3 =  { 'RestaurantName': 'restaurant3',
          'AvailableSeats': '1',
          'SafenessLevel': 'HighRisk'
          }
data4 =  { 'RestaurantName': 'restaurant4',
          'AvailableSeats': '1',
          'SafenessLevel': 'HighRisk'
          }
firebase.post('location/Stuttgart/04-07-2020',data1)
firebase.post('location/Stuttgart/04-07-2020',data2)
firebase.post('location/Stuttgart/04-07-2020',data3)
firebase.post('location/Stuttgart/04-07-2020',data4)
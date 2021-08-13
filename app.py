from flask import Flask, render_template, request,redirect,url_for
import folium as folium
import phonenumbers

from phonenumbers import carrier
from phonenumbers import timezone
from opencage.geocoder import OpenCageGeocode
key="4ced0e5e2f3b4ea9b7e6125c47c037bb"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        phone = request.form["phone"]
        phone_number = phone
        phone1 = phonenumbers.parse(phone_number)
        from phonenumbers import geocoder
        if phonenumbers.is_valid_number(phone1):
            cc=(geocoder.description_for_number(phone1, "en"))

            sp=(carrier.name_for_number(phone1, "en"))

            clock=(timezone.time_zones_for_number(phone1))
            kk = geocoder.description_for_number(phone1, "en")
            geocoder = OpenCageGeocode(key)
            query = str(kk)
            result = geocoder.geocode(query)
            # print(result)
            lat = result[0]["geometry"]["lat"]
            lng = result[0]["geometry"]["lng"]

            mymap = folium.Map(location=[lat, lng], zoom_start=9)
            folium.Marker([lat, lng], popup=kk).add_to(mymap)
            mymap.save("templates/my_location.html")
            return render_template("signup.html", number=phone,country=cc,sp=sp,clock=clock)
        else:
            return render_template("signup.html", number="try again", country="NA", sp="NA", clock="NA")

    else:
        return render_template('index.html')

@app.route('/map')
def mymap():
    return render_template('my_location.html')
@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()


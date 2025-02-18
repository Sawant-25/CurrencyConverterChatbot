from flask import Flask, request, jsonify
import requests
import os
app=Flask(__name__)
@app.route('/',methods=['POST'])
def index():
    data=request.get_json()
    # print(data)
    try:
       source_currency=data['queryResult']['parameters']['unit-currency']['currency']
       amount=data['queryResult']['parameters']['unit-currency']['amount']
       target_currency=data['queryResult']['parameters']['currency-name']
       target_currency = target_currency[0] if isinstance(target_currency, list) else target_currency

       # print(source_currency)
       # print(amount)
       # print(target_currency)

    except KeyError as e:
        print(f"Missing key: {e}")
        return "<h1>Error: Missing data</h1>"


    cf = fetch_conversion_factor(source_currency,target_currency)
    # If the API returns a valid response containing a conversion_rate, then cf will contain the actual numeric conversion rate (e.g., 74.83 if converting USD to INR).
    # If the conversion rate is not found, or there is an issue with the API, cf will be None


    final_amount=amount * cf
    final_amount=round(final_amount,2)

    response={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    print("Final Amount after conversion:" ,final_amount)
    # we are returning the amount again back to chatbot to display , for that we use jsonify.
    return jsonify(response)
    # return "<h1>Hello Flask</h1>"


def fetch_conversion_factor(source,target):
    # target = target[0] if isinstance(target, list) else target  # Ensure it's a string
    url = "https://v6.exchangerate-api.com/v6/f5bf64574d1085ebd931f64d/pair/{}/{}".format(source,target)
    print("Fetching URL:", url)  # Debugging print

    response = requests.get(url)

    if response.status_code==200:
        print("Response Text: ",response.text)
        try:
            response_data=response.json()
            print(response_data)

            if 'conversion_rate' in response_data:
                return response_data['conversion_rate']
            else:
                print("Error: Conversion rate not found in the response.")
                return None
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response")
            return  None
    else:
        print(f"Error: {response.status_code}- {response.text}")




#     url = f"https://v6.exchangerate-api.com/v6/YOUR_API_KEY/pair/{source}/{target}"
#     https://v6.exchangerate-api.com/v6/f5bf64574d1085ebd931f64d/pair/USD/INR this is hardcoded means it is only convert the currrencies from USD to INR. We need to make it dyanamic.


if __name__ =="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

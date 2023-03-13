import requests
import simplejson as json
import json
import logging
from syx.BetApi import *
from syx.SyxDb import *
from syx.models import *
from syx.SyxApi import *


class OwnPay:
  def __init__(self, baseurl="https://payment-gateway-uat.ownpay.co.za",paymentgatewayurl="https://payment-gateway-uat.ownpay.co.za/",proxyconfig=None, requestlibrary=requests): # we need to have the requestlibrary declared in order for us to use timing, when the locust devs created it the extended the class so that it can be useed for timing, not using is okay if we dont want to access the timing info, fo anywere we nned to use locust we need the request library
      self.baseurl = baseurl
      self.paymentgatewayurl = paymentgatewayurl
      self.proxyconfig = proxyconfig
      self.requestlibrary = requestlibrary
      print(f"""Proxy Config :  {self.proxyconfig}""")


  def RequestPaymentSimulator(self)->str:
    postbody = f"""{{   "ClientId":"client",   "ClientSecret":"secret",   "MerchantId":1}}"""
    response = ""
    jpostbody = ""
    try:
      endpoint = f"{self.baseurl}/api/Authenticate"
      logging.debug(f"Converting {postbody} to json")
      jpostbody = json.loads(postbody)
      logging.debug(f"Posting {jpostbody} to endpoint: {endpoint}")
      response = self.requestlibrary.post(endpoint, headers={"Accept":"*/*", "Content-Type":"application/json"}, json = jpostbody, proxies=self.proxyconfig, verify=False, timeout=600)
      jresponsebody = json.loads(response.content)
      accessToken = jresponsebody["Access_token"]
      print (f"""Endpoint 1 : {endpoint} Response code : ***** {response.status_code}""")
      return accessToken
    except:
      logging.error(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
      raise Exception(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")


  def PaymentDetails1(self, acesstoken)->str:   #(self, acesstoken:str)->str:# type annotation access token : string - change > str to dict for dictionary
    # '''
      
    
    
    # '''
    postbody = f"""{{   "ClientId":"client",   "ClientSecret":"secret",   "MerchantId":1,   "Amount":1,   "CustomerEmailAddress":"test@test.com",   "InternalRef":"IN000",   "CustomerFirstName":"Auto",   "CustomerSurname":"Mate"}}"""
    token = f"""{acesstoken}"""
    response = ""
    jpostbody = ""
    endpoint = f"""{self.paymentgatewayurl}/api/Payment"""
    jpostbody = json.loads(postbody)
    try:
      jpostbody = json.loads(postbody)
      response = self.requestlibrary.post(endpoint, headers={"Authorization":f"Bearer {acesstoken}"}, json = jpostbody,proxies=self.proxyconfig, verify=False, timeout=600)
      jresponsebody = json.loads(response.content)
      cPaymentRef = jresponsebody["Data"]["PaymentReference"]
      cPaymentProcessURL = jresponsebody["Data"]["PaymentUrl"]
      cPaymentRequest = jresponsebody["Data"]["PaymentRequestId"]
      cClientVerificationToken = jresponsebody["Data"]["QrCodeUrl"]
      print (f"""Endpoint 2 : {endpoint} Response code : ***** {response.status_code}""")
      return cPaymentRef, cPaymentRequest
    except:
      logging.error(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
      raise Exception(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
#  cntrl + space


  def PaymentDetails2(self, acesstoken:str)->str:# type annotation access token : string - change > str to dict for dictionary
    # '''
      
    
    
    # '''
    postbody = f"""{{   "ClientId":"client",   "ClientSecret":"secret",   "MerchantId":1,   "Amount":1,   "CustomerEmailAddress":"test@test.com",   "InternalRef":"IN000",   "CustomerFirstName":"Auto",   "CustomerSurname":"Mate"}}"""
    token = f"""{acesstoken}"""
    response = ""
    jpostbody = ""
    endpoint = f"""{self.paymentgatewayurl}/api/Payment"""
    jpostbody = json.loads(postbody)
    response = self.requestlibrary.post(endpoint, headers={"Authorization":f"Bearer {acesstoken}"}, json = jpostbody,proxies=self.proxyconfig, verify=False, timeout=600) # ,headers={"Authorization":f"Bearer {token}"},
    jresponsebody = json.loads(response.content)
    cPaymentRef = jresponsebody["Data"]["PaymentReference"]
    cPaymentProcessURL = jresponsebody["Data"]["PaymentUrl"]
    cPaymentRequest = jresponsebody["Data"]["PaymentRequestId"]
    cClientVerificationToken = jresponsebody["Data"]["QrCodeUrl"]
    print (f"""Endpoint 3 : {endpoint} Response code : ***** {response.status_code}""")

    return cPaymentRef, cPaymentRequest
#  cntrl + space


  def OwnPayBankPayment(self, cPaymentRequest, cPaymentRef)->str:
    params = f'strategyId=1&paymentModel%5BStrategyId%5D=-1&paymentModel%5BPaymentId%5D={cPaymentRequest}&paymentModel%5BPaymentDetails%5D%5BMerchantId%5D=1&paymentModel%5BPaymentDetails%5D%5BPaymentReference%5D={cpaymentRef}&paymentModel%5BPaymentDetails%5D%5BMerchantName%5D=Hollywood&paymentModel%5BPaymentDetails%5D%5BAmount%5D=1&paymentModel%5BPaymentDetails%5D%5BMerchantLogo%5D=Hollywoodbets%20Logos-12.png&paymentModel%5BPaymentDetails%5D%5BTransactionId%5D='
    endpoint = f"""https://clientui-uat.ownpay.co.za/Home/InitiatePayment"""
    try:
      response = self.requestlibrary.post(endpoint, headers={"Accept":"application/json, text/javascript, */*; q=0.01", "Accept-Encoding":"gzip, deflate, br", "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data = params, proxies=self.proxyconfig, verify=False, timeout=600)
      paymentDetails = response.content
      print (f"""Endpoint 4 : {endpoint} Response code : ***** {response.status_code}""")
      return paymentDetails
    except:
      logging.error(f"Unable to reach endpoint{endpoint}. Postbody used: {params}. Response received {response}")
      raise Exception(f"Unable to reach endpoint{endpoint}. Postbody used: {params}. Response received {response}")


  def PaymentCreateAuth(self, PaymentDetailsJson)->str:
    postbody = PaymentDetailsJson
    response = ""
    jpostbody = ""
    endpoint = f"""https://clientui-uat.ownpay.co.za/AuthRequest/CreateAuthRequest"""
    jpostbody = json.loads(postbody)
    logging.debug(f"Posting {jpostbody} to endpoint: {endpoint}")
    try:
      response = self.requestlibrary.post(endpoint,  headers={"Accept":"application/json, text/javascript, */*; q=0.01", "Accept-Encoding":"gzip, deflate, br", "Content-Type":"application/json"}, json = jpostbody, proxies=self.proxyconfig, verify=False, timeout=600)
      jresponsebody = json.loads(response.content)
      createAuthDetails = {"cTransactionId":jresponsebody["Resource"]["PaymentDetails"]["TransactionId"],
                          "cPaymentRequestID":jresponsebody["Resource"]["PaymentId"],
                          "cPaymentReference":jresponsebody["Resource"]["PaymentDetails"]["PaymentReference"]}
      print (f"""Endpoint 5 : {endpoint} Response code : ***** {response.status_code}""")
      return createAuthDetails
    except:
      logging.error(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
      raise Exception(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
  

  def Payment(self, AuthDetails)->str:
    postbody = {"ActionData":"{\"Username\":\"45234\",\"Password\":\"34534\",\"Cancel\":false,\"CaptchaText\":\"\"}","PaymentDetails":{"Amount":1,"MerchantId":1,"PaymentReference":f"""{AuthDetails["cPaymentReference"]}""","TransactionId":f"""{AuthDetails["cTransactionId"]}"""},"PaymentId":f"""{AuthDetails["cPaymentRequestID"]}""","StrategyId":1}
    response = ""
    jpostbody = ""
    endpoint = f"""https://clientui-uat.ownpay.co.za/AuthRequest/CreateAuthRequest"""
    try:
      response = self.requestlibrary.post(endpoint,  headers={"Accept":"application/json, text/javascript, */*; q=0.01", "Accept-Encoding":"gzip, deflate, br", "Content-Type":"application/json"}, json = postbody, proxies=self.proxyconfig, verify=False, timeout=600)
      jresponsebody = json.loads(response.content)
      print (f"""Endpoint 6 : {endpoint} Response code : ***** {response.status_code}""")
    except:
          logging.error(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")
          raise Exception(f"Unable to reach endpoint{endpoint}. Postbody used: {jpostbody}. Response received {response}")


# v = OwnPay()
v = OwnPay(proxyconfig={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}) # can pass proxy as parameter here to run mitm / charles
accessToken = v.RequestPaymentSimulator()
cpayment = v.PaymentDetails1(acesstoken=accessToken)
cpaymentRef = cpayment[0]
# print (f"""cpaymentref response {cpaymentRef}""")
cpaymentReq = cpayment[1]
# print (f"""cpaymentrequest response {cpaymentReq}""")
paymentDetails = v.OwnPayBankPayment(cPaymentRequest= cpaymentReq, cPaymentRef= cpaymentRef) # cntrl space
paycreateauthdetails = v.PaymentCreateAuth(PaymentDetailsJson=paymentDetails)
v.Payment(AuthDetails=paycreateauthdetails)

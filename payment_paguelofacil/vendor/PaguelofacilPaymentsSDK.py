# import jwt
import base64

class PaguelofacilPaymentsSDK:

    PAGUELOFACIL_PAYMENTS_SANDBOX_APPLICATION_URL = 'https://sandbox.paguelofacil.com'
    PAGUELOFACIL_PAYMENTS_APPLICATION_URL = 'https://secure.paguelofacil.com'

    def __init__(self, access_key, secret_key, environment):
        self.access_key = access_key
        self.secret_key = secret_key
        self.environment = environment

    def get_payment_url(self):
        base = self.PAGUELOFACIL_PAYMENTS_APPLICATION_URL if self.environment == 'production' else self.PAGUELOFACIL_PAYMENTS_SANDBOX_APPLICATION_URL
        return "{}/LinkDeamon.cfm?{}".format(base, self.generate_payment_token())
    
    
    def generate_payment_token(self):
        ''' Parse Payment Data to correct data types and add additional data '''
        payment_data = {
            'CCLW' : str(self.access_key),
            'CMTN' : float(self.payment_data['amount']),
            'CDSC' : str(self.payment_data['merchant_reference']),
            'merchant_reference': str(self.payment_data['merchant_reference']),
            'merchant_return_url': str(self.payment_data['merchant_return_url']),
        }

        if 'merchant_notification_url' in self.payment_data:
            payment_data['merchant_notification_url'] = str(self.payment_data['merchant_notification_url'])

        if 'preselected_aspsp' in self.payment_data:
            payment_data['preselected_aspsp'] = str(self.payment_data['preselected_aspsp'])
        
        if 'preselected_locale' in self.payment_data:
            payment_data['preselected_locale'] = str(self.payment_data['preselected_locale'])
        url_retor = payment_data.get('merchant_return_url').encode("utf-8").hex()
        monto_ready = '{0:.2f}'.format(payment_data.get('CMTN'))
        url_next = 'CCLW=' + payment_data.get('CCLW') + '&CMTN=' + str(monto_ready) + '&CDSC=' + payment_data.get('CDSC') + '&RETURN_URL=' + str(url_retor)
        return url_next



    # @staticmethod
    # def decode_payment_token(token, secret_key):
    #     try:
    #         return jwt.decode(token, secret_key, algorithms=['HS256'])
    #     except jwt.exceptions.InvalidSignatureError as identifier:
    #         return False
    
    ''' MARK: Property accessors '''
    @property
    def payment_data(self):
        return self.__payment_data
    
    @payment_data.setter
    def payment_data(self, value):
        self.__payment_data = value

    @property
    def access_key(self):
        return self.__access_key
    
    @access_key.setter
    def access_key(self, value):
        self.__access_key = value

    @property
    def secret_key(self):
        return self.__secret_key

    @secret_key.setter
    def secret_key(self, value):
        self.__secret_key = value
    
    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value):
        self.__environment = value


        

    

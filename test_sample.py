import cryptoFunctions
import gmailConnect

def testRoundTripCrypto():
    data = cryptoFunctions.encrypt("hello", "world", "helloworld")
    cryptoFunctions.saveConfigFile(data, "testOutput.yaml")
    roundTripData = cryptoFunctions._decrypt("testOutput.yaml", "helloworld")
    assert roundTripData['username'] == "hello"
    assert roundTripData['password'] == "world"

def testIMAPConnect():
    gmailConnect.connectIMAP()
    assert 1 == 1

def hello():
    return "hello"

def test_hello():
    assert hello() == "hello"
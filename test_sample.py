import cryptoFunctions

def testRoundTripCrypto():
    data = cryptoFunctions.encrypt("hello", "world", "helloworld")
    cryptoFunctions.saveConfigFile(data, "testOutput.yaml")
    roundTripData = cryptoFunctions.decrypt("testOutput.yaml", "helloworld")
    assert roundTripData['username'] == "hello"
    assert roundTripData['password'] == "world"


def hello():
    return "hello"

def test_hello():
    assert hello() == "hello"
from es_alertt import should_alert

def test_above_thresold():
    assert should_alert(4, 3) == True

def test_at_threshold():
    assert should_alert(0, 3) == False
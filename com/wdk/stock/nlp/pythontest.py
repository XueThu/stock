str = "Line1-abcdef.json.concept.test.cool"
print( str.split('.') )
print( str.split('.',1 ))
print( str.split('.',2 ))
print( str.split('.',3 ))

print( str.split('.')[len(str.split('.'))-1] )


enterprise_token_key_value = {}

enterprise_token_key_value = {"1":"value 1"}
enterprise_token_key_value["1"] += " added by 2"
enterprise_token_key_value.update({"2":"22"})
enterprise_token_key_value.update({"1":"new value"})
enterprise_token_key_value.update({"1":"new value 2"})
enterprise_token_key_value.setdefault('3','33')

print(enterprise_token_key_value)
# print (enterprise_token_key_value.get("4"))

for i in range(0,2):
    print(i)
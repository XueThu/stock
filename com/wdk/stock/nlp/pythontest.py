# str = "Line1-abcdef.json.concept.test.cool"
# print( str.split('.') )
# print( str.split('.',1 ))
# print( str.split('.',2 ))
# print( str.split('.',3 ))
# print( str.split('.')[len(str.split('.'))-1] )

# enterprise_token_key_value = {}
# enterprise_token_key_value = {"1":"value 1"}
# enterprise_token_key_value["1"] += " added by 2"
# enterprise_token_key_value.update({"2":"22"})
# enterprise_token_key_value.update({"1":"new value"})
# enterprise_token_key_value.update({"1":"new value 2"})
# enterprise_token_key_value.setdefault('3','33')
# print(enterprise_token_key_value)


# dict的值类型是变化的,非常自由
dict_set = {"message": ": success", "item": [1,2,3]}
print(dict_set['message'])

for item in dict_set['item']:
    print(item)

dict_set['item'].append(4)
print(dict_set['item'])

# for i in range(0,2):
#     print(i)
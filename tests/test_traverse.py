import unittest
import flows


class TestTraverse(unittest.TestCase):
    
    def test_match_path(self):

        tests = (
            (["match"], ["match"], True),
            (["match"], ["no-match"], False),
            ([(0, 2)], ["[]"], False),
            ([(1, 2)], ["[]"], True),
            (["match", (0,2)], ["match", "[]"], False),
            (["match", (1,2)], ["match", "[]"], True),
            (["match", "match-2", (0,2)], ["match", "match-2", "[]"], False),
            (["match", "match-2", (1,2)], ["match", "match-2", "[]"], True),
            (["match", "match-2", (1,2)], ["match", "no-match", "[]"], False)
        )
        
        for path, target_path, result in tests:
            with self.subTest(path=path, 
                              target_path=target_path, 
                              result=result):
                self.assertTrue(flows.match_path(path, target_path) == result)
    
    def test_to_path(self):

        schema = {
            "key" : {
                "repeating" : False,
                "parent" : None
            },
            "next-key" : {
                "repeating" : False,
                "parent" : "key"
            },
            "repeating-key" : {
                "repeating" : True,
                "parent" : "key"
            }
        }
        
        tests = (
            (schema, "key", ["key"]),
            (schema, "next-key", ["key", "next-key"]),
            (schema, "repeating-key", ["key", "repeating-key", "[]"])
        )
        
        for schema, key, result in tests:
            with self.subTest(schema=schema, 
                              key=key, 
                              result=result):
                self.assertEqual(flows.to_path(schema, key), result)

    def test_traverse(self):

        deep_obj = {'k': {'k': [{'k': 'v'}, {'k': 'v'}]}}
        new_deep_obj = {'k': {'k': [{'k': "new-v"}, {'k': "new-v"}]}}
        last_deep_obj = {'k': {'k': [{'k': 'v'}, {'k': "new-v"}]}}
        first_deep_obj = {'k': {'k': [{'k': "new-v"}, {'k': 'v'}]}}
        
        change_all_v = lambda p, v: "new-v" if v == 'v' else v
        change_last_v = lambda p, v: "new-v" if v == 'v' \
                        and p == ['k', 'k', (1, 2), 'k'] else v
        change_first_v = lambda p, v: "new-v" if v == 'v' \
                        and p == ['k', 'k', (0, 2), 'k'] else v

        tests = (
            ({}, None, {}),
            ({'k': 'v'}, None, {'k': 'v'}),
            (deep_obj, None, deep_obj),
            (deep_obj, change_all_v, new_deep_obj),
            (deep_obj, change_last_v, last_deep_obj),
            (deep_obj, change_first_v, first_deep_obj)
        )
        
        for obj, callback, result in tests:
            with self.subTest(obj=obj, 
                              callback=callback, 
                              result=result):
                self.assertEqual(flows.traverse(obj, callback=callback), result)

    def test_traverse_add_item(self):
        schema = {'k':{"repeating":False, "parent":None}}

        tests = (
            ({}, schema, 'k', 'i', {'k':'i'}),
            ({'k1':'i1'}, schema, 'k', 'i', {'k':'i', 'k1': 'i1'})
        )
        for obj, schema, key, item, result in tests:
            with self.subTest(obj=obj,
                              schema=schema,
                              key=key,
                              item=item,
                              result=result):
                self.assertEqual(flows.traverse_add_item(obj, schema, key, item), result)

    def test_validate_item(self):

        tests = (
            ('k', 'i', {'k':{"repeating":True}}, ['i']),
            ('k', 'i', {'k':{"repeating":False}}, 'i')
        )

        for key, item, schema, result in tests:
            with self.subTest(key=key,
                              item=item,
                              schema=schema,
                              result=result):
                self.assertEqual(flows.validate_item(key, item, schema), result)

    def test_add_item(self):

        tests = (
            ({}, 'k', 'i', {'k':'i'}),
            ({'k':['i']}, 'k', 'i', {'k':['i', 'i']}),
            ({'k':['i']}, 'k', ['i'], {'k':['i', 'i']})
        )

        for value, key, item, result in tests:
            with self.subTest(value=value,
                              key=key,
                              item=item,
                              result=result):
                self.assertEqual(flows.add_item(value, key, item), result)

    
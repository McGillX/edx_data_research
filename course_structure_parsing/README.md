Insert the edx course_structure-prod-analytics .json file into mongodb database for aggregation

The single JSON object will be split into sub JSON objects, in which all the first level keys will become 
the _id of its object value

For instance, the single document:

```json
{
  "i4x://McGillX/CHEM181x/chapter/031268b19dd846beb542205b15bbb80f": {
    "category": "chapter", 
    "children": [
      "i4x://McGillX/CHEM181x/sequential/8fb7ae4fdb4544f5a85f129ac4cda7ac"
    ], 
    "metadata": {
      "display_name": "Exit Survey", 
      "start": "2014-04-02T17:00:00Z"
    }
  }, 
  "i4x://McGillX/CHEM181x/chapter/0c3523abccf34c08aff06cfa21bd68df": {
    "category": "chapter", 
    "children": [
      "i4x://McGillX/CHEM181x/sequential/7c0001183b8b4f8fb0e3e523e865a36d", 
      "i4x://McGillX/CHEM181x/sequential/707157217d144777884da1618d1d08e9", 
      "i4x://McGillX/CHEM181x/sequential/7873c19d76e84cc897651d5188ed5a82", 
      "i4x://McGillX/CHEM181x/sequential/f83e1dcf83164a3da7ed1401385da8dc"
    ], 
    "metadata": {
      "display_name": "Week 9: Diet & Disease", 
      "start": "2014-03-19T17:00:00Z"
    }
  }, 

  ...

}
```

will become many documents in mongodb:

```json
{
  _id: "i4x://McGillX/CHEM181x/chapter/031268b19dd846beb542205b15bbb80f",
  "category": "chapter", 
  "children": [
    "i4x://McGillX/CHEM181x/sequential/8fb7ae4fdb4544f5a85f129ac4cda7ac"
  ], 
  "metadata": {
    "display_name": "Exit Survey", 
    "start": "2014-04-02T17:00:00Z"
  }
}
```

```json
{
  _id: "i4x://McGillX/CHEM181x/chapter/0c3523abccf34c08aff06cfa21bd68df",
  "category": "chapter", 
  "children": [
    "i4x://McGillX/CHEM181x/sequential/7c0001183b8b4f8fb0e3e523e865a36d", 
    "i4x://McGillX/CHEM181x/sequential/707157217d144777884da1618d1d08e9", 
    "i4x://McGillX/CHEM181x/sequential/7873c19d76e84cc897651d5188ed5a82", 
    "i4x://McGillX/CHEM181x/sequential/f83e1dcf83164a3da7ed1401385da8dc"
  ], 
  "metadata": {
    "display_name": "Week 9: Diet & Disease", 
    "start": "2014-03-19T17:00:00Z"
  }
}
```

```
...
```

### Categories

# course
## chapter
### sequential (lesson)
#### vertical (activity)
##### html problem dicussion video poll_question word_cloud wrapper conditional





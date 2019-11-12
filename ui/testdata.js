const be$ = from([
  {type: 'group_receive', message: {id: 3, text: 'sup', created: '20:39', sign: 'ghbkasjdkflasdfjlas;djfaskldfjasl', parents: [2]}},
  {type: 'group_receive', message: {id: 1, text: 'adsf', created: 'igår 20:39', sign: 'ahbk'}},
  {type: 'group_receive', message: {id: 4, text: 'hello world', created: '2019-09-07 20:39', sign: 'ahbk', parents: [1,2]}},
  {type: 'group_receive', message: {id: 2, text: 'qwer', created: '13:37', sign: 'frans', parents: [1]}},
  {type: 'group_receive', message: {id: 5, text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,', created: '13:37', sign: 'frans', parents: [1]}},
  {type: 'group_receive', message: {id: 5, text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,', created: '13:37', sign: 'frans', parents: [1]}},
  {type: 'group_receive', message: {id: 5, text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,', created: 'i förrgår 13:37', sign: 'frans', parents: [1]}},
  {type: 'group_receive', message: {id: 5, text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,', created: '13:37', sign: 'frans', parents: [1]}},
  {type: 'group_receive', message: {id: 5, text: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s,', created: new Date(), sign: 'frans', parents: [1]}},
])



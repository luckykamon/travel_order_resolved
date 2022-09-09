import nlp_perso

assert nlp_perso.test(data="Je souhaite aller à Rennes depuis Paris",
                      prov="Paris", dest="Rennes"), "Test1 error"
assert nlp_perso.test(data="Je souhaite partir depuis Paris et aller à Rennes",
                      prov="Paris", dest="Rennes"), "Test2 error"
assert nlp_perso.test(data="Je souhaite aller a Rennes en partant de Paris",
                      prov="Paris", dest="Rennes"), "Test3 error"
assert nlp_perso.test(data="Je souhaite aller de Rennes à Paris",
                      prov="Rennes", dest="Paris"), "Test4 error"
assert nlp_perso.test(data="Je souhaite partir de Paris pour aller à Rennes",
                      prov="Paris", dest="Rennes"), "Test5 error"
assert nlp_perso.test(data="Je souhaite aller à Rennes à partir de Paris",
                      prov="Paris", dest="Rennes"), "Test6 error"
assert nlp_perso.test(data="Je souhaite faire Paris Rennes",
                      prov="Paris", dest="Rennes"), "Test7 error"
assert nlp_perso.test(data="Je souhaite faire Rennes Paris",
                      prov="Rennes", dest="Paris"), "Test8 error"
assert nlp_perso.test(data="Je souhaite aller a Rennes en provenance de Paris",
                      prov="Paris", dest="Rennes"), "Test9 error"
assert nlp_perso.test(data="Je souhaite prendre un train en provenance de Paris et a destination de Rennes",
                      prov="Paris", dest="Rennes"), "Test10 error"
assert nlp_perso.test(data="Je souhaite prendre un train a destination de Rennes et en provenance de Paris",
                      prov="Paris", dest="Rennes"), "Test11 error"
assert nlp_perso.test(data="Je souhaite un hamburger",
                      prov="Paris", dest="Rennes") == False, "Test12 error"
assert nlp_perso.test(data="",
                      prov="", dest="") == False, "Test13 error"

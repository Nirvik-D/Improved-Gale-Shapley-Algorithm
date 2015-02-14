import copy
import time
import json
with open('10_couples_male.json') as f:
    guyprefers = json.load(f)
with open('10_couples_female.json') as f2:
    galprefers = json.load(f2)
guys = sorted(guyprefers.keys())
gals = sorted(galprefers.keys())
print(guyprefers)
print(galprefers)
def sorting(messed_order,correct_order):
    return [x for x in correct_order if x in messed_order]
def duplicate_remover(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
def check(engaged):
    inverseengaged = dict((v,k) for k,v in engaged.items())
    for she, he in engaged.items():
        shelikes = galprefers[she]
        shelikesbetter = shelikes[:shelikes.index(he)]
        helikes = guyprefers[he]
        helikesbetter = helikes[:helikes.index(she)]
        for guy in shelikesbetter:
            guysgirl = inverseengaged[guy]
            guylikes = guyprefers[guy]
            if guylikes.index(guysgirl) > guylikes.index(she):
                print("%s and %s like each other better than "
                      "their present partners: %s and %s, respectively"
                      % (she, guy, he, guysgirl))
                return False
        for gal in helikesbetter:
            girlsguy = engaged[gal]
            gallikes = galprefers[gal]
            if gallikes.index(girlsguy) > gallikes.index(he):
                print("%s and %s like each other better than "
                      "their present partners: %s and %s, respectively"
                      % (he, gal, she, girlsguy))
                return False
    return True
 
def matchmaker():
    count = 0
    guysfree = guys[:]
    engaged  = {}
    guyprefers2 = copy.deepcopy(guyprefers)
    galprefers2 = copy.deepcopy(galprefers)
    while guysfree:
        probability_to_break_up = 0
        guy = guysfree.pop(0)
        guyslist = guyprefers2[guy]
        gal = guyslist.pop(0)        
        fiance = engaged.get(gal)
        if not fiance:
            # She's free
            guysfree.append(guy)
            if len(guysfree) > 0:
                _guys_free = sorting(guysfree, galprefers2[gal])
                probability_to_break_up = (_guys_free.index(guy))/len(_guys_free)                
                if probability_to_break_up <= 0.5:
                    engaged[gal] = guy
                    print("  %s and %s" % (guy, gal))
                    guysfree.pop(guysfree.index(guy))
                else:
                    guysfree.pop(guysfree.index(guy))
                    guysfree.append(guy)
        else:
            # The guy proposes to an engaged girl
            galslist = galprefers2[gal]
            if galslist.index(fiance) > galslist.index(guy):
                # She prefers new guy
                engaged[gal] = guy
                print("  %s dumped %s for %s" % (gal, fiance, guy))
                if guyprefers2[fiance]:
                    # Ex has more girls to try
                    guysfree.append(fiance)
                    count += 1
            else:
                # She is faithful to old fiance
                if guyslist:
                    # Look again
                    guysfree.append(guy)
    print()
    print('Number of break ups for new algorithm: ', count)
    '''with open("...Location.../Records_new.txt", "a") as text_file:
        text_file.writelines("Number of break ups recorded for 100 couples: %s\n" %count)'''
    return engaged
print()
print('Engagements:')
engaged = matchmaker()
 
print('\nCouples:')
print('  ' + ',\n  '.join('%s is engaged to %s' % couple
                          for couple in sorted(engaged.items())))
print()
print('Engagement stability check PASSED'
      if check(engaged) else 'Engagement stability check FAILED')

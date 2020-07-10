l1 = [
  'designs',
  'fascists',
  'precious',
  'purists',
  'recents',
  'register',
  'rellist',
  'reports',
  'requests',
  'resiny',
  'resist',
  'resistance',
  'resisted',
  'resister',
  'resistere',
  'resisting',
  'resists',
  'resulted',
  'sist',
  'stresses',
  'supremacists']


def contiguous_string_matches(main_s, s_compare):
    for i in range(len(s_compare)):
        if s_compare[i] != main_s[i]:
            return False

    return True


csm = contiguous_string_matches
l2 = [w for w in l1 if csm('resistance', w)]
print(l2)

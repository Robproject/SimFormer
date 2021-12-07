# SimFormer
Exact or approximate transformer calculations with phasor diagram

Input:
|V2|, |S|(VA), Load %, p.f. %, 'lead' or 'lag', a, Z1, Z2, ZC, and whether the core is 'before' Z1 or if it's 'center'ed    

Example with 240v, 2.4KVA, 80% load, unity p.f. (lead/lag doesn't matter in this case), N1/N2 = 10, and respective impedances in rectangular form:
 SimForm(240, 2400, .8, 1, "lag", 10, 1.5 + 2.5j, 0.02 + 0.03j, 6000 + 8000j, 'center' )

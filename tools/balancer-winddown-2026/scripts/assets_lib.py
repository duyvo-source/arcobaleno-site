from common import *
V3="0xbA1333333333a1BA1108E8412f11850A5C319bA9"
def v3pool(chain,pool,who,n):
    bp_=bal(chain,pool,who,n) or 0; sup=word(call(chain,pool,"totalSupply()","",n))
    r=call(chain,V3,"getPoolTokenInfo(address)",pad(pool),n); h=r[2:]; w=[h[i:i+64] for i in range(0,len(h),64)]
    n_t=int(w[int(w[0],16)//32],16); toks=["0x"+x[24:] for x in w[int(w[0],16)//32+1:][:n_t]]
    off=int(w[2],16)//32; bals=[int(x,16) for x in w[off+1:off+1+n_t]]
    return toks,[b*bp_/sup for b in bals],bp_/sup

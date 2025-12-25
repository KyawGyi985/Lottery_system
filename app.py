from flask import Flask, render_template, request

app = Flask(__name__)

def reduce_number(n):
    """ဂဏန်းတစ်လုံးတည်းကျန်သည်အထိ ပေါင်းခြင်း Logic"""
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def get_lottery_result(number_str):
    """တစ်တန်းချင်းစီအတွက် တွက်ချက်ခြင်း"""
    if not number_str or not number_str.isdigit() or len(number_str) != 6:
        return None # ဂဏန်းမဟုတ်ရင် သို့မဟုတ် ၆ လုံးမပြည့်ရင် None ပြန်မယ်

    # ရှေ့ ၃ လုံး နှင့် နောက် ၃ လုံး ခွဲထုတ်ခြင်း
    front_sum = sum(int(d) for d in number_str[:3])
    back_sum = sum(int(d) for d in number_str[3:])

    # ခြားနားချက်ရှာခြင်း (Absolute Difference)
    diff = abs(front_sum - back_sum)

    # ၉ ကျော်ရင် ပြန်ပေါင်းခြင်း
    final_digit = reduce_number(diff)

    # Small or Big ဆုံးဖြတ်ခြင်း
    size = "Big" if final_digit >= 5 else "Small"
    
    return {
        "input": number_str,
        "raw_diff": diff,
        "final_digit": final_digit,
        "size": size
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    rows = []
    final_result = None
    
    if request.method == 'POST':
        # Form မှ Input ၅ ခုကို ယူမယ်
        inputs = request.form.getlist('lottery_input')
        
        big_count = 0
        small_count = 0
        
        for idx, val in enumerate(inputs):
            res = get_lottery_result(val)
            if res:
                rows.append(res)
                if res['size'] == "Big":
                    big_count += 1
                else:
                    small_count += 1
            else:
                # အမှားပါရင် Empty row ထည့်မယ်
                rows.append({"input": val, "size": "-", "final_digit": "-"})

        # Final Result တွက်ချက်ခြင်း (များရာအနိုင်ယူစနစ်)
        if big_count > small_count:
            final_result = "Big"
        elif small_count > big_count:
            final_result = "Small"
        else:
            final_result = "Draw" # သရေကျခဲ့ရင် (ဂဏန်းမပြည့်တာပါခဲ့ရင် ဖြစ်နိုင်)

    # ပထမဆုံးအကြိမ် ဖွင့်ရင် အလွတ်ပြမယ်
    if not rows:
        rows = [{"input": "", "size": "", "final_digit": ""} for _ in range(5)]

    return render_template('index.html', rows=rows, final_result=final_result)

if __name__ == '__main__':
    app.run(debug=True)
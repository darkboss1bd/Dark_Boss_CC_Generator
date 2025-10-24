import random
import os
import webbrowser
from datetime import datetime, timedelta

class AdvancedDarkBossCCGenerator:
    def __init__(self):
        self.brands = {
            'Visa': ['4'],
            'Mastercard': ['51', '52', '53', '54', '55'],
            'Amex': ['34', '37'],
            'Discover': ['6011', '65']
        }
        
    def luhn_check(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0

    def generate_expiry_date(self):
        current_year = datetime.now().year
        month = random.randint(1, 12)
        year = current_year + random.randint(1, 5)
        return f"{month:02d}/{year}"

    def generate_cvv(self, brand):
        if brand == 'Amex':
            return str(random.randint(1000, 9999))  # 4-digit CVV for Amex
        else:
            return str(random.randint(100, 999))    # 3-digit CVV for others

    def generate_cc(self, bin_number=None):
        if bin_number is None:
            brand = random.choice(list(self.brands.keys()))
            bin_number = random.choice(self.brands[brand])
        else:
            brand = self.identify_brand(bin_number)
        
        # Generate remaining digits
        cc_number = bin_number
        while len(cc_number) < 15:
            cc_number += str(random.randint(0, 9))
        
        # Calculate Luhn check digit
        for check_digit in range(10):
            test_cc = cc_number + str(check_digit)
            if self.luhn_check(test_cc):
                expiry = self.generate_expiry_date()
                cvv = self.generate_cvv(brand)
                return {
                    'number': test_cc,
                    'expiry': expiry,
                    'cvv': cvv,
                    'brand': brand
                }
        
        return None

    def identify_brand(self, bin_number):
        for brand, bins in self.brands.items():
            for b in bins:
                if bin_number.startswith(b):
                    return brand
        return 'Unknown'

    def generate_single_cc(self):
        print("\n[+] Generating Single CC...")
        cc_data = self.generate_cc()
        if cc_data:
            print(f"[+] Valid CC Generated:")
            print(f"    Number: {cc_data['number']}")
            print(f"    Expiry: {cc_data['expiry']}")
            print(f"    CVV: {cc_data['cvv']}")
            print(f"    Brand: {cc_data['brand']}")
            return cc_data
        else:
            print("[-] Failed to generate valid CC")
            return None

    def generate_multi_cc(self, count=10):
        print(f"\n[+] Generating {count} CCs...")
        cc_list = []
        for i in range(count):
            cc_data = self.generate_cc()
            if cc_data:
                cc_list.append(cc_data)
                print(f"[{i+1}] {cc_data['number']} | {cc_data['expiry']} | {cc_data['cvv']} | {cc_data['brand']}")
        
        print(f"\n[+] Generated {len(cc_list)} valid CCs")
        return cc_list

    def validate_cc(self, cc_number):
        print(f"\n[+] Validating CC: {cc_number}")
        if self.luhn_check(cc_number):
            print("[+] CC is VALID")
            return True
        else:
            print("[-] CC is INVALID")
            return False

    def generate_multi_bin(self, count=5):
        print(f"\n[+] Generating {count} BIN numbers...")
        bin_list = []
        for i in range(count):
            brand = random.choice(list(self.brands.keys()))
            bin_num = random.choice(self.brands[brand])
            # Extend to 6-digit BIN
            while len(bin_num) < 6:
                bin_num += str(random.randint(0, 9))
            bin_list.append({'bin': bin_num, 'brand': brand})
            print(f"[{i+1}] {bin_num} ({brand})")
        
        return bin_list

    def generate_html_report(self, cc_data_list, filename="darkboss_cc_report.html"):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dark Boss CC Generator Report</title>
            <style>
                body {{
                    font-family: 'Courier New', monospace;
                    background: linear-gradient(135deg, #0c0c0c, #1a1a2e);
                    color: #00ff00;
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(0, 0, 0, 0.8);
                    border: 2px solid #00ff00;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 0 20px #00ff00;
                }}
                .header {{
                    text-align: center;
                    padding: 20px;
                    border-bottom: 2px solid #00ff00;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    color: #ff0000;
                    text-shadow: 0 0 10px #ff0000;
                    margin: 0;
                    font-size: 2.5em;
                }}
                .header h2 {{
                    color: #00ff00;
                    margin: 10px 0;
                    font-size: 1.5em;
                }}
                .info-section {{
                    background: rgba(0, 255, 0, 0.1);
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .cc-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                .cc-table th {{
                    background: #006600;
                    color: #00ff00;
                    padding: 12px;
                    text-align: left;
                    border: 1px solid #00ff00;
                }}
                .cc-table td {{
                    padding: 12px;
                    border: 1px solid #00ff00;
                    background: rgba(0, 255, 0, 0.05);
                }}
                .cc-table tr:hover td {{
                    background: rgba(0, 255, 0, 0.1);
                }}
                .brand-visa {{ color: #1a1f71; font-weight: bold; }}
                .brand-mastercard {{ color: #eb001b; font-weight: bold; }}
                .brand-amex {{ color: #2e77bc; font-weight: bold; }}
                .brand-discover {{ color: #ff6000; font-weight: bold; }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding: 20px;
                    border-top: 1px solid #00ff00;
                    color: #888;
                }}
                .footer a {{
                    color: #00ff00;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
                .timestamp {{
                    color: #888;
                    font-size: 0.9em;
                    text-align: right;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🦊 DARK BOSS CC GENERATOR</h1>
                    <h2>Powered by DARKBOSS1BD</h2>
                </div>
                
                <div class="info-section">
                    <h3>📞 Contact Information:</h3>
                    <p>• Telegram ID: <a href="https://t.me/darkvaiadmin">https://t.me/darkvaiadmin</a></p>
                    <p>• Telegram Channel: <a href="https://t.me/windowspremiumkey">https://t.me/windowspremiumkey</a></p>
                    <p>• Hacking/Cracking Website: <a href="https://crackyworld.com/">https://crackyworld.com/</a></p>
                </div>

                <div class="timestamp">
                    Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </div>

                <h3>💳 Generated Credit Cards:</h3>
                <table class="cc-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Card Number</th>
                            <th>Expiry Date</th>
                            <th>CVV</th>
                            <th>Brand</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for i, cc_data in enumerate(cc_data_list, 1):
            brand_class = f"brand-{cc_data['brand'].lower()}"
            html_content += f"""
                        <tr>
                            <td>{i}</td>
                            <td>{cc_data['number']}</td>
                            <td>{cc_data['expiry']}</td>
                            <td>{cc_data['cvv']}</td>
                            <td class="{brand_class}">{cc_data['brand']}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
                
                <div class="footer">
                    <p><strong>Warning:</strong> This tool is for educational purposes only. Use responsibly.</p>
                    <p>© 2024 Dark Boss Security Tools | https://crackyworld.com/</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[+] HTML report generated: {filename}")
        return filename

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                   DARK BOSS CC GENERATOR                     ║
    ║                   Powered by DARKBOSS1BD                     ║
    ║                                                              ║
    ║    ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ███████╗║
    ║    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗██╔════╝║
    ║    ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║███████╗║
    ║    ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║╚════██║║
    ║    ██████╔╝██║  ██║██║  ██║██║  ██╗██║  ██║╚██████╔╝███████║║
    ║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝║
    ║                                                              ║
    ║      Telegram: https://t.me/darkvaiadmin                     ║
    ║     Channel: https://t.me/windowspremiumkey                  ║
    ║        Website: https://crackyworld.com/                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def main():
    generator = AdvancedDarkBossCCGenerator()
    
    while True:
        display_banner()
        print("[x] 1) Generate single valid CC")
        print("[x] 2) Generate multi valid CC (generate CC list)")
        print("[x] 3) CC validator")
        print("[x] 4) Generate Multi BIN Number")
        print("[x] 5) Generate HTML Report")
        print("[x] 6) Exit")
        
        choice = input("\n[A] Please Enter an option: ").strip()
        
        if choice == '1':
            cc_data = generator.generate_single_cc()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            try:
                count = int(input("[A] Enter number of CCs to generate: "))
                cc_list = generator.generate_multi_cc(count)
                
                # Ask if user wants HTML report
                if cc_list and input("\nGenerate HTML report? (y/n): ").lower() == 'y':
                    filename = generator.generate_html_report(cc_list)
                    if input("Open HTML report in browser? (y/n): ").lower() == 'y':
                        webbrowser.open(f'file://{os.path.abspath(filename)}')
            except ValueError:
                print("[-] Please enter a valid number")
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            cc = input("[A] Enter CC number to validate: ").strip()
            generator.validate_cc(cc)
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            try:
                count = int(input("[A] Enter number of BINs to generate: "))
                generator.generate_multi_bin(count)
            except ValueError:
                print("[-] Please enter a valid number")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            try:
                count = int(input("[A] Enter number of CCs for HTML report: "))
                cc_list = []
                for i in range(count):
                    cc_data = generator.generate_cc()
                    if cc_data:
                        cc_list.append(cc_data)
                
                if cc_list:
                    filename = generator.generate_html_report(cc_list)
                    if input("Open HTML report in browser? (y/n): ").lower() == 'y':
                        webbrowser.open(f'file://{os.path.abspath(filename)}')
                else:
                    print("[-] No valid CCs generated")
            except ValueError:
                print("[-] Please enter a valid number")
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            print("\n[+] Thank you for using Dark Boss CC Generator!")
            print("[+] Visit: https://crackyworld.com/")
            break
        
        else:
            print("[-] Invalid option! Please choose 1-6")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

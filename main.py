import pywhatkit.whats as pwk
from src.extras.safety import is_installed
from src.extras.pdf import sendwhatspdf



if __name__ == "__main__":
    print(is_installed("pywhatkit"))

    for i in range(5):
        sendwhatspdf(
            receiver="+21653400838",
            pdf_path="attach/pdf/sample.pdf",
            caption=f"promo wido {i}",
            wait_time=15,
            tab_close=True
        )






import os
import pandas as pd
from prophet import Prophet
from crewai.tools import BaseTool

class ProphetTool(BaseTool):
    name: str = "predict_cyclone_temp_with_prophet"
    description: str = (
        "Membaca data industrial dari Excel, melakukan prediksi suhu Cyclone Gas Outlet "
        "untuk 1 jam ke depan menggunakan Prophet, dan mengembalikan report ringkas."
    )

    def _run(self, file_path: str) -> str:
        try:
            absolute_file_path = os.path.abspath(file_path)

            df = pd.read_excel(absolute_file_path)
            df = df[['time', 'Cyclone_Gas_Outlet_Temp']].rename(columns={'time': 'ds', 'Cyclone_Gas_Outlet_Temp': 'y'})
            df['ds'] = pd.to_datetime(df['ds'])
            
            m = Prophet()
            m.fit(df)
            
            future = m.make_future_dataframe(periods=12, freq='5min')
            forecast = m.predict(future)
            
            future_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12)
            
            rata_rata_prediksi = future_forecast['yhat'].mean()
            max_prediksi = future_forecast['yhat_upper'].max()
            
            report_data = (
                f"Prediksi berhasil dijalankan.\n"
                f"Rata-rata prediksi suhu (yhat) 1 jam ke depan: {rata_rata_prediksi:.2f}\n"
                f"Batas atas suhu maksimal (yhat_upper): {max_prediksi:.2f}\n\n"
                f"Detail 5 prediksi terakhir:\n"
                f"{future_forecast.tail(5).to_markdown()}"
            )
            
            return report_data

        except Exception as e:
            return f"Terjadi kesalahan saat memproses prediksi: {str(e)}"
package xyz.lintd.portr_act;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    final String TAG = "PRTR";

    ImageButton iBtn_act;
    TextView tvState;
    TextView tvLast;
    FetchQStateTask onlytask;
    OkHttpClient httpClient;
    SimpleDateFormat dateFormat;
    boolean is_alive;
    Timer jtime;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        is_alive = false;
        dateFormat = new SimpleDateFormat("HH:mm:ss");
        httpClient = new OkHttpClient();
        tvState = findViewById(R.id.textView);
        tvLast = findViewById(R.id.textView2);
        iBtn_act = findViewById(R.id.imgBtn_piact);
        iBtn_act.setOnClickListener(this::onIBtnActClick);
    }

    @Override
    protected void onResume() {
        super.onResume();
        jtime = new Timer();
        jtime.schedule(new TimerTask() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        onIBtnActClick(null);
                    }
                });
            }
        }, 200, 1000 * 60);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (jtime != null) {
            jtime.cancel();
            jtime = null;
        }
    }

    public void onIBtnActClick(View v) {
        if (onlytask == null || onlytask.getStatus() == AsyncTask.Status.FINISHED) {
            onlytask = new FetchQStateTask();
            tvState.setText(R.string.pend_prompt);
            onlytask.execute(BuildConfig.PORTR_Q_URL);
        }
    }

    private class FetchQStateTask extends AsyncTask<String, Integer, String> {
        protected String doInBackground(String... urls) {
            Request request = new Request.Builder()
                    .url(BuildConfig.PORTR_Q_URL)
                    .build();
            try (Response response = httpClient.newCall(request).execute())
            {
                return response.body().string();
            } catch (Exception e) {
                Log.d(TAG, "send request fail", e);
            }
            return null;
        }

        protected void onProgressUpdate(Integer... progress) {
        }

        protected void onPostExecute(String result) {
            // this is executed on the main thread after the process is over
            // update your UI here
            if (null == result) {
                tvState.setText(R.string.send_req_err_prompt);
            } else {
                tvState.setText(R.string.good_res_prompt);
                tvLast.setText("last fetch: " + dateFormat.format(new Date()));
                if (result.equals("ALIVE")) {
                    if (!is_alive) {
                        is_alive = true;
                        iBtn_act.setImageResource(android.R.drawable.presence_online);
                    }
                } else {
                    if (is_alive) {
                        is_alive = false;
                        iBtn_act.setImageResource(android.R.drawable.presence_offline);
                    }
                }
            }
        }
    }
}

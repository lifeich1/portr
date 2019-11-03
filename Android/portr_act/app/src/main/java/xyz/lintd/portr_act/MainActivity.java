package xyz.lintd.portr_act;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    ImageButton iBtn_act;
    TextView tvState;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvState = findViewById(R.id.textView);
        iBtn_act = findViewById(R.id.imgBtn_piact);
        iBtn_act.setOnClickListener(this::onIBtnActClick);
    }

    public void onIBtnActClick(View v) {
        // TODO send
    }
}

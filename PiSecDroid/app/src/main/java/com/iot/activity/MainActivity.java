package com.iot.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.iot.common.UrlBuilder;
import com.iot.gmartin.alarmaiot_soa.R;
import com.iot.rest.Callback;
import com.iot.rest.NetworkTask;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Pantalla principal
 */
public class MainActivity extends AppCompatActivity {
    private EditText code;
    private Button button;

    private Timer timer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        this.code = (EditText) findViewById(R.id.code);
        this.button = (Button) findViewById(R.id.button);

        initButtons();
    }

    /**
     * Configura los botones de navegación y encendido / apagado de la alarma
     */
    private void initButtons() {
        this.button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new NetworkTask(new Callback() {
                    @Override
                    public void run(String result) {
                        if (result != null) {
                            String password = code.getText().toString();
                            if (result.equals(password)) {
                                Intent intent = new Intent(MainActivity.this, OperationsActivity.class);
                                intent.putExtra("password", password);
                                startActivity(intent);
                            } else {
                                AlertDialog alertDialog = new AlertDialog.Builder(MainActivity.this).create();
                                alertDialog.setTitle("Error");
                                alertDialog.setMessage("Código inválido!");
                                alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                                        new DialogInterface.OnClickListener() {
                                            public void onClick(DialogInterface dialog, int which) {
                                                dialog.dismiss();
                                            }
                                        });
                                alertDialog.show();
                            }
                        }
                    }
                }).execute(UrlBuilder.build("password"));
            }
        });
    }
}

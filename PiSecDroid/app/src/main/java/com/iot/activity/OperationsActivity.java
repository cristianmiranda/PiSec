package com.iot.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Switch;

import com.iot.common.ShakeDetector;
import com.iot.gmartin.alarmaiot_soa.R;
import com.iot.common.UrlBuilder;
import com.iot.rest.Callback;
import com.iot.rest.NetworkTask;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Pantalla de operaciones
 */
public class OperationsActivity extends AppCompatActivity implements SensorEventListener {
    private Switch statusSwitch;
    private Button takePictureButton;
    private Button seeLastPictureButton;
    private EditText codeText;
    private Button sendCodeButton;
    private ImageView picture;

    private Timer timer;
    private String password;
    private Sensor mSensorProx;
    private Sensor mSensorAcc;
    private SensorManager mSensorManager;
    private ShakeDetector mShakeDetector;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_operations);

        this.statusSwitch = (Switch) findViewById(R.id.statusSwitch);
        this.takePictureButton = (Button) findViewById(R.id.takePictureButton);
        this.seeLastPictureButton = (Button) findViewById(R.id.seeLastPictureButton);
        this.codeText = (EditText) findViewById(R.id.codeText);
        this.sendCodeButton = (Button) findViewById(R.id.sendCodeButton);
        this.picture = (ImageView) findViewById(R.id.picture);
        this.mSensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        this.mSensorProx = mSensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
        this.mSensorAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

        initShakeDetector();
        initButtons();
        initTimer();
    }

    @Override
    protected void onStart() {
        super.onStart();
        Intent intent = getIntent();
        this.password = intent.getStringExtra("password");
    }

    /**
     * Inicia el timer que consulta la temperatura cada 1500 milisegundos
     */
    private void initTimer() {
        this.timer = new Timer();
        TimerTask timerTask = new TimerTask() {
            @Override
            public void run() {
                execute();
            }
        };
        this.timer.schedule(timerTask, 0, 1500);
    }

    /**
     * Ejecuta la consulta y actualización segun datos en la alarma
     */
    private void execute() {
        new NetworkTask(new Callback() {
            @Override
            public void run(String result) {
                statusSwitch.setOnCheckedChangeListener(null);
                statusSwitch.setChecked(result != null && result.equals("1"));
                initSwitchButton();
            }
        }).execute(UrlBuilder.build("status"));
    }

    /**
     * Inicializa el comportamiento de los botones
     */
    private void initButtons() {
        initSwitchButton();
        sendCodeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                password = codeText.getText().toString();
                new NetworkTask(new Callback() {
                    @Override
                    public void run(String result) {
                        AlertDialog alertDialog = new AlertDialog.Builder(OperationsActivity.this).create();
                        alertDialog.setMessage("Código actualizado con éxito.");
                        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                                new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        dialog.dismiss();
                                    }
                                });
                        alertDialog.show();
                    }
                }).execute(UrlBuilder.build("password/" + password));
            }
        });
        seeLastPictureButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                getLastPicture("auto");
            }
        });
        takePictureButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                takeManualPicture();
            }
        });
    }

    private void takeManualPicture() {
        new NetworkTask(new Callback() {
            @Override
            public void run(String result) {
                getLastPicture("manual");
            }
        }).execute(UrlBuilder.build("picture/manual/take"));
    }

    private void getLastPicture(String mode) {
        new NetworkTask(new Callback() {
            @Override
            public void run(String result) {
                byte[] decodedString = Base64.decode(result, Base64.DEFAULT);
                Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                picture.setImageBitmap(decodedByte);
            }
        }).execute(UrlBuilder.build("picture/" + mode));
    }

    private void initSwitchButton() {
        statusSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, final boolean isChecked) {
                String status = isChecked ? "on" : "off";
                new NetworkTask().execute(UrlBuilder.build(status + "/" + password));
            }
        });
    }

    protected void onResume() {
        super.onResume();
        mSensorManager.registerListener(this, mSensorProx, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(mShakeDetector, mSensorAcc,	SensorManager.SENSOR_DELAY_UI);
    }

    protected void onPause() {
        super.onPause();
        mSensorManager.unregisterListener(this);
        mSensorManager.unregisterListener(mShakeDetector);
    }

    private void initShakeDetector() {
        this.mShakeDetector = new ShakeDetector();
        this.mShakeDetector.setOnShakeListener(new ShakeDetector.OnShakeListener() {
            @Override
            public void onShake(int count) {
                takeManualPicture();
            }
        });
    }

    /**
     * En caso de ser detectado un movimiento en el sensor de proximidad, se apaga la alarma.
     * @param event
     */
    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_PROXIMITY) {
            if (event.values[0] == 0) {
                statusSwitch.setChecked(false);
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }
}

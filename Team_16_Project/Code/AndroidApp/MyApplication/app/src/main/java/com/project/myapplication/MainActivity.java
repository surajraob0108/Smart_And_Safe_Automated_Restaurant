package com.project.myapplication;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private TextView safenessLevel;
    private Button setButton;
    private Spinner locationSpinner;
    private TextView restaurant1,restaurant2,restaurant3,restaurant4;

    DatabaseReference databaseReader = FirebaseDatabase.getInstance().getReference("location");
    String currentDate = new SimpleDateFormat("dd-MM-yyyy", Locale.getDefault()).format(new Date());
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        safenessLevel = (TextView) findViewById(R.id.safeness_text);
        setButton = (Button) findViewById(R.id.Button);
        locationSpinner = (Spinner) findViewById(R.id.spinner);
        restaurant1 = (TextView) findViewById(R.id.restaurant1);
        restaurant2 = (TextView) findViewById(R.id.restaurant2);
        restaurant3 = (TextView) findViewById(R.id.restaurant3);
        restaurant4 = (TextView) findViewById(R.id.restaurant4);

        setButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String location = locationSpinner.getSelectedItem().toString();

                databaseReader.child(location).child(currentDate)
                        .addValueEventListener(new ValueEventListener() {
                            @Override
                            public void onDataChange(DataSnapshot dataSnapshot) {
                                int restaurant1_seats = 3, restaurant2_seats = 3, restaurant3_seats = 3, restaurant4_seats=3;
                                String safeness_level = "NoRisk";
                                for(DataSnapshot locationInfo : dataSnapshot.getChildren()) {
                                    HashMap map = (HashMap) locationInfo.getValue();
                                    safeness_level = (String)map.get("SafenessLevel");

                                    if (map.get("RestaurantName").equals("0"))
                                    {
                                        restaurant1_seats = Integer.valueOf(String.valueOf(map.get("AvailableTables")));
                                    }
                                    else if (map.get("RestaurantName").equals("1"))
                                    {
                                        restaurant2_seats = Integer.valueOf((String)map.get("AvailableTables"));
                                    }
                                    else if (map.get("RestaurantName").equals("2"))
                                    {
                                        restaurant3_seats = Integer.valueOf(String.valueOf(map.get("AvailableTables")));
                                    }
                                    else
                                    {
                                        restaurant4_seats = Integer.valueOf(String.valueOf(map.get("AvailableTables")));
                                    }
                                }
                                safenessLevel.setTextColor(Color.parseColor("#000000"));
                                if (safeness_level.equals("HighRisk") || safeness_level.equals("SevereRisk")) {
                                    safenessLevel.setText("SAFE_LEVEL : " + safeness_level);
                                    int colour = Color.parseColor("#FF0000");
                                    safenessLevel.setBackgroundColor(colour);
                                }
                                else if (safeness_level.equals("ModerateRisk")) {
                                    safenessLevel.setText("SAFE_LEVEL : " + safeness_level);
                                    int colour = Color.parseColor("#FFFF00");
                                    safenessLevel.setBackgroundColor(colour);
                                    colour = Color.parseColor("#000000");
                                    safenessLevel.setTextColor(colour);
                                }
                                else
                                {
                                    safenessLevel.setText("SAFE_LEVEL : " + safeness_level);
                                    int colour = Color.parseColor("#3CB371");
                                    safenessLevel.setBackgroundColor(colour);
                                }

                                restaurant1.setText("LA-BRUSCHETTA"+ "   FREE_TABLES : " + String.valueOf(restaurant1_seats));
                                restaurant2.setText("INDIA-HOUSE" +"          FREE_TABLES : " + String.valueOf(restaurant2_seats));
                                restaurant3.setText("RISTORANTE           FREE_TABLES : " + String.valueOf(restaurant3_seats));
                                restaurant4.setText("PIZZERIA                  FREE_TABLES : " + String.valueOf(restaurant4_seats));
                            }

                            @Override
                            public void onCancelled(@NonNull DatabaseError databaseError) {
                            }
                        });
            }
        });
    }
}
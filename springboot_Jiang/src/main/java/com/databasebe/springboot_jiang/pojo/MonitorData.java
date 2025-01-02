package com.databasebe.springboot_jiang.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Table(name="monitor_data")
@Entity
@Data
public class MonitorData {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long Id;
    @Column(name = "monitor_id")
    private Integer monitor_id;
    @Column(name = "collect_time")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime collect_time;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Column(name = "upload_time")
    private LocalDateTime upload_time;
    @Column(name = "wind_direction")
    private String wind_direction;
    @Column(name = "wind_speed")
    private Double wind_speed;
    @Column(name = "humidity")
    private Double humidity;
    @Column(name = "rainfall")
    private Double rainfall;
    @Column(name = "air_temperature")
    private Double air_temperature;
    @Column(name = "air_pressure")
    private Double air_pressure;
    @Column(name = "scene_type")
    private String scene_type;
}

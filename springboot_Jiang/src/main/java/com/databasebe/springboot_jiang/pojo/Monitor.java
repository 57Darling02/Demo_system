package com.databasebe.springboot_jiang.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.persistence.Column;
import jakarta.persistence.Id;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class Monitor {
    @Id
    @Column(name = "monitor_id")
    private Integer monitor_id;
    @Column(name = "password")
    private String password;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime alive_time;
}

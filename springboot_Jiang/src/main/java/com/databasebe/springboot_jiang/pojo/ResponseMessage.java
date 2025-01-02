package com.databasebe.springboot_jiang.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.http.HttpStatus;
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ResponseMessage<T> {
    private Integer code;
    private String message;
    private T data;

    public static <T> ResponseMessage<T> success(T data) {
        return new ResponseMessage(HttpStatus.OK.value(),"success",data);
    }
    public static ResponseMessage error(Integer code, String message) {
        return new ResponseMessage(code,message,null);
    }


}

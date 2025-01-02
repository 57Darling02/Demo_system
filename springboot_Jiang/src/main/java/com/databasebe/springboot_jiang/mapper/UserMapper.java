package com.databasebe.springboot_jiang.mapper;

import com.databasebe.springboot_jiang.pojo.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
@Mapper
public interface UserMapper {
    @Select("select * from user where username = #{username}")
    User findByUsername(String username);
    @Insert("insert into user (username,password,create_time,update_time) " +
            "values (#{username},#{password},now(),now())")
    void register(String username, String password);
}

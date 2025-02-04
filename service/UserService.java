package service;

import model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import repository.UserRepository;

import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User createUserService(User user) {
        // Implement logic to create a new user
        return userRepository.save(user);
    }

    public List<User> createUsersWithListInputService(List<User> users) {
        // Implement logic to create multiple users with an input list
        return userRepository.saveAll(users);
    }

    public User getUserByNameService(String username) {
        // Implement logic to get user by username
        return userRepository.findByUsername(username);
    }

    public User updateUserService(String username, User user) {
        // Implement logic to update user
        User existingUser = userRepository.findByUsername(username);
        if(existingUser != null) {
            existingUser.setEmail(user.getEmail());
            existingUser.setPassword(user.getPassword());
            existingUser.setPhone(user.getPhone());
            return userRepository.save(existingUser);
        }
        return null;
    }

    public void deleteUserService(String username) {
        // Implement logic to delete user
        User user = userRepository.findByUsername(username);
        if(user != null) {
            userRepository.delete(user);
        }
    }

    public boolean loginUserService(String username, String password) {
        // Implement login logic
        User user = userRepository.findByUsername(username);
        return user != null && user.getPassword().equals(password);
    }

    public void logoutUserService() {
        // Implement logout logic
        // This could involve session management
    }
}

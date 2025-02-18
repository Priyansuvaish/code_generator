api result: ### API Tag: Pet

1. **Controller Layer Tasks:**
   - Implement endpoints for:
     - `PUT /pet`: Update an existing pet.
     - `POST /pet`: Add a new pet to the store.
     - `GET /pet/findByStatus`: Retrieve pets by status.
     - `GET /pet/findByTags`: Retrieve pets by tags.
     - `GET /pet/{petId}`: Retrieve a pet by ID.
     - `POST /pet/{petId}`: Update a pet with form data.
     - `DELETE /pet/{petId}`: Delete a pet.
     - `POST /pet/{petId}/uploadImage`: Upload an image for a pet.

2. **Service Layer Tasks:**
   - Implement methods:
     - `updatePet(Pet pet)`: Validate and update pet details.
     - `addPet(Pet pet)`: Validate and save new pet details.
     - `findPetsByStatus(String status)`: Retrieve list of pets based on status.
     - `findPetsByTags(List<String> tags)`: Retrieve list of pets based on tags.
     - `getPetById(Long petId)`: Find and return the pet by ID.
     - `updatePetWithForm(Long petId, String name, String status)`: Update pet's information using form data.
     - `deletePet(Long petId)`: Remove pet by ID.
     - `uploadFile(Long petId, byte[] image, String metadata)`: Handle the image upload process.

3. **Repository Layer Tasks:**
   - Set up JPA repositories for:
     - `PetRepository`: To handle database operations related to the `Pet` entity.

4. **Data Models:**
   - Utilize the components:
     - `Pet`: Represents the pet object with properties such as `id`, `name`, `category`, `photoUrls`, `tags`, and `status`.
     - `Category`: Represents pet categories.
     - `Tag`: Represents tags associated with pets.

5. **Database Schema:**
   - Design tables for data entities:
     - `pet` table with fields matching the `Pet` schema.
     - `category` table.
     - `tags` table with a many-to-many relationship with the `pet` table.

### API Tag: Store

1. **Controller Layer Tasks:**
   - Implement endpoints for:
     - `GET /store/inventory`: Get pet inventories by status.
     - `POST /store/order`: Place an order for a pet.
     - `GET /store/order/{orderId}`: Find purchase order by ID.
     - `DELETE /store/order/{orderId}`: Delete purchase order by ID.

2. **Service Layer Tasks:**
   - Implement methods:
     - `getInventory()`: Return the inventory status.
     - `placeOrder(Order order)`: Validate and process a new order request.
     - `getOrderById(Long orderId)`: Retrieve order details by order ID.
     - `deleteOrder(Long orderId)`: Remove order by order ID.

3. **Repository Layer Tasks:**
   - Set up JPA repository for:
     - `OrderRepository`: To handle database operations for the `Order` entity.

4. **Data Models:**
   - Utilize the components:
     - `Order`: Represents order details with properties like `id`, `petId`, `quantity`, `shipDate`, `status`, and `complete`.

5. **Database Schema:**
   - Design a table for `order` with fields matching the Order schema.

### API Tag: User

1. **Controller Layer Tasks:**
   - Implement endpoints for:
     - `POST /user`: Create user.
     - `POST /user/createWithList`: Create multiple users.
     - `GET /user/login`: Log user in.
     - `GET /user/logout`: Log user out.
     - `GET /user/{username}`: Get user details by username.
     - `PUT /user/{username}`: Update user details.
     - `DELETE /user/{username}`: Delete user by username.

2. **Service Layer Tasks:**
   - Implement methods:
     - `createUser(User user)`: Validate and create a new user.
     - `createUsersWithList(List<User> users)`: Batch creation of multiple users.
     - `loginUser(String username, String password)`: Authenticate the user.
     - `logoutUser()`: Handle user logout.
     - `getUserByName(String username)`: Retrieve user details.
     - `updateUser(User user)`: Validate and update user information.
     - `deleteUser(String username)`: Remove user by username.

3. **Repository Layer Tasks:**
   - Set up JPA repository for:
     - `UserRepository`: To manage database access for the `User` entity.

4. **Data Models:**
   - Use the component:
     - `User`: Details of the user with properties like `id`, `username`, `firstName`, `lastName`, `email`, `password`, `phone`, and `userStatus`.

5. **Database Schema:**
   - Design a table for `user` with relevant fields as per the User schema.
```
